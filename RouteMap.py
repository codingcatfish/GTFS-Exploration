#Visualizes routes on a geopandas map.
from pathlib import Path
import geopandas as gpd
from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import pandas as pd
import osmnx as ox
import contextily as ctx
from random import randint

data_path = Path.cwd() / "GTFSData"
hexstrings = "1234567890ABCDEF"

def read(file_path):
    return pd.read_csv(data_path / file_path)

def randColor():
    str = "#"
    for i in range(6):
        str+=hexstrings[randint(0,15)]
    return str

#Set city to the location you're visualizing
city = "Manhattan"

#Plot 1, dot map
df_stops = read("stops.txt")
geometry = [Point(xy) for xy in zip(df_stops['stop_lon'], df_stops['stop_lat'])]
gdf_stops = gpd.GeoDataFrame(df_stops, geometry=geometry)
df_stops.crs = 'EPSG:4326' #lattitude longitude projection
admin = ox.geocode_to_gdf(city) #City boundary

f, ax = plt.subplots(1,1,figsize=(15,15))
admin.plot(ax=ax, color = 'none', edgecolor = 'k')
gdf_stops.plot(ax=ax, alpha = 0.2)


#Plot 2: Map all or selected route.
df_route = read("routes.txt")
df_shapes = read("shapes.txt")

# Transform the shape into a GeoDataFrame
df_shapes['shape_pt_lat'] = df_shapes['shape_pt_lat'].astype(float)
df_shapes['shape_pt_lon'] = df_shapes['shape_pt_lon'].astype(float)

df_shapes['geometry'] = df_shapes.apply(lambda row: Point(row['shape_pt_lon'], row['shape_pt_lat']), axis=1)
df_shapes = gpd.GeoDataFrame(df_shapes[['shape_id', 'geometry']])
df_shapes.crs = 4326

#Transform shapes into a line string
gdf_shapes = gpd.GeoDataFrame(df_shapes[['shape_id', 'geometry']].groupby(by = 'shape_id').agg(list))
gdf_shapes = gdf_shapes[[len(g)>1 for g in gdf_shapes['geometry'].to_list()]]
gdf_shapes['geometry'] = gdf_shapes['geometry'].apply(lambda x: LineString(x))
gdf_shapes = gpd.GeoDataFrame(gdf_shapes)


# map the means of transport
df_trips = read("trips.txt")[['route_id', 'shape_id']].drop_duplicates()
gdf_shapes = gdf_shapes.merge(df_trips, left_index = True, right_on = 'shape_id')
gdf_shapes = gdf_shapes.groupby(by = "route_id")

# create the visuals in matplotlib
f, ax = plt.subplots(1,1,figsize=(12,12))

cax = admin.plot(ax=ax, edgecolor = 'k', color = 'none')
cax = admin.plot(ax=ax, edgecolor = 'k', alpha = 0.2)

#Plot a single route
gdf_shapes.get_group("M3").plot(ax=ax, color = '#16417C', alpha = 0.9, linewidth = 1) 

#Plot all routes
for route, item in gdf_shapes:
    gdf_shapes.get_group(route).plot(ax=ax, color = randColor(), alpha = 0.9, linewidth = 1)    

ax.axis('off')
ctx.add_basemap(ax, alpha = 0.8, crs = 4326, url = ctx.providers.CartoDB.DarkMatterNoLabels)
plt.tight_layout()
plt.show()

