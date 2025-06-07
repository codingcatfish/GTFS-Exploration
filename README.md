# GTFS-Exploration
## Introduction
This repository contains several programs that explore GTFS data. 
You can:
- Calculate total distance traveled by all vehicles
- Calculate individual vehicle distance and travel time statistics
- Create and save a schedule sorted by departure time
- Create and save schedules for individual vehicles
- Plot vehicle routes on a map

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
Libraries used include math, pandas, and pathlib. Plotting also requires contextily, geopandas, matplotlib, osmnx, random, seaborn, and shapely.

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
save_combined_data = False      # Setting this to True will save the combined schedules to a CSV file.
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
1. **bus_schedule:** Creates a separate daily schedule for each vehicle (unique block_id) and displays trip information. Trips are ordered by arrival_time and have their distances shown. The resulting data frame is grouped by vehicle with the header:

        trip_id | departure_time | arrival_time | Trip distance (in miles)

A sample output for the Manhattan Transit system is shown below. 
- **block_id** refers to the unique vehicle this schedule references.
- **trip_id** shows the different trips this vehicle takes in one day. They are ordered by arrival_time.
- **arrival_time** and **departure_time** of each trip is shown.
- **trip distances** in miles are also shown.
```
# Sample schedule for vehicle 34545487
      block_id                      trip_id  departure_time    arrival_time  Trip distance (in miles)
5504  34545487  OF_H4-Weekday-003000_M7_201 0 days 01:11:00 0 days 00:30:00                  7.633725
5615  34545487  OF_H4-Weekday-010500_M7_201 0 days 02:25:00 0 days 01:45:00                  8.104641
5506  34545487  OF_H4-Weekday-016000_M7_201 0 days 03:19:00 0 days 02:40:00                  7.633725
5617  34545487  OF_H4-Weekday-022500_M7_201 0 days 04:23:00 0 days 03:45:00                  8.104641
5510  34545487  OF_H4-Weekday-031900_M7_201 0 days 06:03:00 0 days 05:19:00                  7.633725
5621  34545487  OF_H4-Weekday-038300_M7_201 0 days 07:25:00 0 days 06:23:00                  8.104641
```

3. **bus_info:** Creates a dataframe containing important **daily** statistics for each vehicle, including **travel distance**, **time**, and **number of stops**. The table header contains:

        block_id | miles traveled | travel time | total stops
```
# Sample Daily Statistics output
      block_id  Trip distance (in miles)  Travel time (in hours)  total stops
0     34545487                 47.215099                6.916667          360
1     34545488                 47.215099                7.383333          360
2     34545489                 78.691832               16.050000          600
```
   

Both outputs can be saved to CSV by setting **save_bus_schedule** and **save_bus_stats** to True for bus_schedule and bus_info, respectively.

3. **Plots histograms** of daily miles traveled and time spent traveling. A sample output of daily distance traveled is shown below. 
<img src="https://github.com/user-attachments/assets/494d6182-d05c-427a-a2b8-c1a78d77d9c1" alt = "First sample output of BusSchedule, a histogram showing the buses' distribution of daily distance travelled (miles)" width=80% height=50%>

### Plot Routes on a Map
Creates two plots to visualize GTFS data overlaying the geopandas map.
1. Dot plot of stops in stops.txt
2. Map containing routes plotted in random colors. You can choose to plot all routes in routes.txt or specify one route to plot.

**User options**
- Set **city** to the location of your GTFS data. This variable determines the base map of the plotted routes.
- If plotting one route only, set **one_route** to that route's name.
```
city = "Manhattan"    # Line 13
one_route = "M3"
```

#### Sample plot of Manhattan Transit System

<img src="https://github.com/user-attachments/assets/c13d672f-c4d5-456e-8959-d7a2467392ea" alt = "Sample output of RouteMap, showing a map of the city of Manhattan with randomly colored routes overlaying it." width=65% height=80%>
