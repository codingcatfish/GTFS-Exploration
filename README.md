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
**GTFS** stands for **General Transit Feed Specification**, a standardized data format for public transportation. The [sample data](https://transitfeeds.com/p/mta/82) provides bus schedules in Manhattan.

## Contents
- [Setting the file path](#Setting-the-file-path)
- [Saving to CSV](#Saving-to-CSV)
- [Data Introduction](#Data-Info)
- [Trip Distance](#Trip-Distance)
- [Link Trips into a Schedule](#Link-Trips-into-a-Schedule)
- [Bus Schedules and Statistics](#Bus-Schedules-and-Statistics)
- [Plot Routes on a Map](#Plot-Routes-on-a-Map)

  
## Usage
### Sample Data
Sample data for Manhattan transport can be downloaded at [https://transitfeeds.com/p/mta/82](https://transitfeeds.com/p/mta/82)

### Libraries
Libraries used include pandas, pathlib, and math. RouteMap also requires geopandas, shapely, matplotlib, osmnx, contextily, and random.

### Setting the file path
> [!WARNING]
> To ensure the correct files are being read, **redefine _data_path_** to the location of the folder that contains your GTFS files. You will need to do this in every script.

Path.cwd() refers to the current working directory, which is the file location of the script.
For example, if you have a folder that contains both your GTFS data in "DataFolder" and the script, you should redefine data_path to the following:
```
# === Change these! ===
data_path = Path.cwd() / "DataFolder"
```

Or you can use an absolute path, starting from the root directory and working your way to the data file:
```
data_path = "/home/downloads/DataFolder/schedules.txt"
```

### Saving to CSV
> [!IMPORTANT]
> Script outputs can be saved to CSV by **setting the save boolean to True.**
> This option exists for **LinkTrips** and **BusSchedule.** 

An example can be found in LinkTrips, line 9:
```
# === Change these! ===
data_path = Path.cwd() / "GTFSData"
save_combined_data = False  # Setting this to True will save the combined schedules to a CSV file.
```

## Files
### Data Info
Provides a preview of the GTFS data.
When imported, it will print out sample rows from the main GTFS files (routes, trips, stops, stop_times, shapes) and explain what each column contains.

### Trip Distance
> [!IMPORTANT]
> Trip Distance is required for **LinkTrips** and **BusSchedule**.

A helper file that estimates the distance in _miles_ traveled each trip. 
Two methods of distance calculation are supported:
1. **Haversine**: Returns straight line distance that accounts for Earth's curvature
2. **Manhattan**: Returns distance that treats longitude and latitude as a grid layout (for roads that follow a street-like layout).

The Haversine method is used by default. This can be toggled in line 14 by setting **haversine_mode** to False.

### Link Trips into a Schedule
Combine trips, stop_times, and stops. The resulting data frame contains the headers:

    trip_id | route_id | stop_sequence | stop_name | arrival_time | departure_time | Trip distance (in miles)

The output can be saved to a CSV in Line 11 by setting **save_combined_data** to True.

### Bus Schedules and Statistics
1. **bus_schedule:** Builds a basic schedule showing schedules for each vehicle (unique block_id). The resulting data frame is grouped by block_id with the header:

        trip_id | departure_time | arrival_time | Trip distance (in miles)

2. **bus_info:** Creates a dataframe containing daily statistics for each vehicle with the header:

        block_id | miles traveled | travel time | total stops

3. **Plots histograms** of miles traveled and travel time each day. Sample outputs are shown below:
<img src="https://github.com/user-attachments/assets/27b80b89-92b7-4c2e-972a-7d86b2945f11" alt = "First sample output of BusSchedule, a histogram showing the buses' distribution of daily travel length (hours)." width=80% height=50%>
<img src="https://github.com/user-attachments/assets/e8f2a764-2e60-4d29-96aa-bdd8efa66110" alt = "First sample output of BusSchedule, a histogram showing the buses' distribution of daily distance travelled (miles)" width=80% height=50%>

 Data can also be saved to csv by uncommenting the last two lines.  

### Plot Routes on a Map
Creates two plots to visualize GTFS data overlaying the geopandas map.
1. Dot plot of stops in stops.txt
2. Map containing routes plotted in random colors. You can choose to plot all routes in routes.txt or specify one route to plot.

> [!WARNING]
> **Redefine _city_** to the correct GTFS data location.

```
city = "Manhattan"    # Line 24
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

<img src="https://github.com/user-attachments/assets/c13d672f-c4d5-456e-8959-d7a2467392ea" alt = "Sample output of RouteMap, showing a map of the city of Manhattan with randomly colored routes overlaying it." width=65% height=80%>
