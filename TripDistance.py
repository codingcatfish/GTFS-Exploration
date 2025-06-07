# Estimates the distance traveled in each trip.
# Supports two methods of distance calculation:
# Haversine: Returns straight line distance that accounts for Earth's curvature
# Manhattan: Returns distance that treats longitude and latitude as a grid layout.

import pandas as pd
from pathlib import Path
from math import  cos, sin, asin, sqrt, pi
data_path = Path.cwd() / "GTFSData"
def read_data(file_path):
    return pd.read_csv(data_path / file_path)

# === Change this! ===
haversine_mode = True   # False: uses MANHATTAN calculation

def haversine(lat1, lat2, lon1, lon2):
    # convert decimal degrees to radians 
    lat1 *= pi/180
    lat2 *= pi/180
    lon1 *= pi/180
    lon2 *= pi/180
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3963.19 # Radius of earth in miles
    return c * r
    

def distance_traveled(file_path):
    shapes = read_data(file_path)
    if 'shape_dist_traveled' in shapes:
        return shapes.groupby("shape_id", sort = False).max()
    else:
        shape_groups = shapes.groupby("shape_id")
        result = {"shape_id":[],"Trip distance (in miles)":[]}
        result = pd.DataFrame(result)

        for shape, frame in shape_groups:
            frame2 = frame.sort_values(by=["shape_pt_sequence"])
            dist = 0
            for i in range(frame2.first_valid_index(), frame2.last_valid_index()): #distance calculation
                # Total shape distance
                if haversine_mode:
                     dist +=haversine(frame2["shape_pt_lat"][i], frame2["shape_pt_lat"][i+1], frame2["shape_pt_lon"][i], frame2["shape_pt_lon"][i+1])
                else: # Manhattan
                    dist +=haversine(frame2["shape_pt_lat"][i], frame2["shape_pt_lat"][i], frame2["shape_pt_lon"][i+1], frame2["shape_pt_lon"][i]) + haversine(frame2["shape_pt_lat"][i+1], frame2["shape_pt_lat"][i], frame2["shape_pt_lon"][i+1], frame2["shape_pt_lon"][i+1])
            result = pd.concat([result, pd.DataFrame([[shape,dist]],columns = result.columns)])
        return result
