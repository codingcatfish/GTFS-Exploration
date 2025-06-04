# GTFS-Exploration
## Introduction
This repository contains several programs that explore GTFS data. 
You can:
- Calculate total distance traveled by all vehicles
- Calculate individual vehicle distance and travel time statistics
- Create and save a schedule sorted by departure time
- Create and save a schedule sorted by individual vehicles
- Plot vehicle routes on a map

Make sure to set the file path correctly for best results.
**GTFS** stands for **General Transit Feed Specification**, a standardized data format for public transportation. The sample data _GTFSData_ provides bus schedules in Manhattan.

## Contents
- [Setting the file path](#Setting-the-file-path)
- [Data Info](#Data-Info)
- [Link Trips](#Link-Trips)
- [Bus Schedules and Statistics](#Bus-Schedules-and-Statistics)
- [Plot Route Map](#Route-Map)
- [Trip Distance](#Trip-Distance)
  
## Usage
### Libraries
Libraries used include pandas, pathlib, and math. RouteMap also requires geopandas, shapely, matplotlib, osmnx, contextily, and random.

### Setting the file path
> [!WARNING]
> To ensure the correct files are being read, **redefine _data_path_** to the location of the folder that contains your GTFS files. You will need to do this in every script.

Path.cwd() refers to the current working directory, which is the file location of the script.
For example, if you have a folder that contains both your GTFS data in "ReadableData" and the script, you should redefine data_path to the following:
```
data_path = Path.cwd() / "ReadableData"
```

Or you can use an absolute path, starting from the root directory and working your way to the data file:
```
data_path = "/home/downloads/ReadableData/schedules.txt"
```

### Data Info
Provides a preview of the GTFS data.
When imported, it will print out sample rows from the main GTFS files (routes, trips, stops, stop_times, shapes) and explain what each column contains.
```
import DataInfo
```

### Link Trips
Combine trips, stop_times, and stops. The resulting data frame contains the headers:

    trip_id | route_id | stop_sequence | stop_name | arrival_time | departure_time | Trip distance (in miles)

Data can be saved to a csv by uncommenting the last line.

### Bus Schedules and Statistics
1. **bus_schedule:** Builds a basic schedule showing schedules for each vehicle (unique block_id). The resulting data frame is grouped by block_id and contains:

        trip_id | departure_time | arrival_time | Trip distance (in miles)

2. **bus_info:** Creates a dataframe containing daily statistics for each vehicle with the header:

        block_id | miles traveled | travel time | total stops

 Data can be saved to csv by uncommenting the last lines.  

### Plot Route Map
Creates two plots to visualize GTFS data overlaying the geopandas map.
1. Dot plot of stops in stops.txt
2. Map containing routes plotted in random colors. You can choose to plot all routes in routes.txt or specify one route to plot.

> [!WARNING]
> **Redefine _city_** to the GTFS data location so the correct city is shown.

```
city = "Manhattan"
```

**Plotting one route**

Set **M3** to the route you want to plot and comment out the loop below _#Plot all routes_.
```
#Plot a single route
gdf_shapes.get_group("M3").plot(ax=ax, color = '#16417C', alpha = 0.9, linewidth = 1) 

#Plot all routes
for route, item in gdf_shapes:
    gdf_shapes.get_group(route).plot(ax=ax, color = randColor(), alpha = 0.9, linewidth = 1)   
```

#### Sample plot of Manhattan Transit System

<img src="https://github.com/user-attachments/assets/c13d672f-c4d5-456e-8959-d7a2467392ea" alt = "Sample output of RouteMap, showing a map of the city of Manhattan with randomly colored routes overlaying it." width=50% height=50%>

### Trip Distance
A helper file that estimates the distance in _miles_ traveled each trip.
Two methods of distance calculation are supported:
1. **Haversine**: Returns straight line distance that accounts for Earth's curvature
2. **Manhattan**: Returns distance that treats longitude and latitude as a grid layout (for roads that follow a street-like layout).

The Haversine method is used by default, line 43 contains the Manhattan method instead.
