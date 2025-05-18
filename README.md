# GTFS-Exploration
Explore GTFS data and calculate vehicle schedules, distance traveled, and more.
To ensure the correct files are being read, redefine data_path to the location of the folder that contains your GTFS files.
### Data info
Provides a preview of the GTFS data.
Prints out sample rows from the main GTFS files (routes, trips, stops, stop_times, shapes) and explains what each column means.

### GTFS Route Map
Creates two plots to visualize GTFS data overlaying the geopandas map. Set city to the location of the GTFS files you're visualizing.
1. Dot plot of stops in stops.txt
2. Map containing routes plotted in random colors. You can choose to plot all routes in routes.txt or specify one route to plot.

### Trip Distance
Estimates the distance traveled in each trip. The distance_traveled method requires a file path to shapes.txt.
Two methods of distance calculation are supported:
1. **Haversine**: Returns straight line distance that accounts for Earth's curvature
2. **Manhattan**: Returns distance that treats longitude and latitude as a grid layout (for roads that follow a street-like layout).
The Haversine method is used by default, uncomment line 43 if you want to use the Manhattan method instead.

### Link Trips
Combine trips, stop_times, and stops. The resulting data frame contains trip_id, route_id, stop_sequence, stop_name, arrival_time, departure_time, and Trip distance (in miles).

### Bus Schedules
1. Builds a basic schedule showing schedules for each vehicle (unique block_id). The resulting data frame is grouped by block_id and contains trip_id, departure_time, arrival_time, and Trip distance (in miles). Requires Trip Distance for calculations.
2. Creates a dataframe containing daily statistics for each vehicle, with miles traveled, hours traveled, and total stops.
