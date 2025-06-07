#Builds a basic schedule showing which trips stop where and when.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import TripDistance as distCalc
from pathlib import Path

pd.set_option('display.width',1000)
pd.set_option('display.max_columns',100)

# === Change these! ===
data_path = Path.cwd() / "GTFSData"
save_bus_schedule = False
save_bus_stats = False

def read(file_path):
    return pd.read_csv(data_path / file_path)

# Organizing the data into "schedule"
schedule = read("trips.txt")[["trip_id", "block_id", "shape_id"]]

stop_times = read("stop_times.txt")[["trip_id", "stop_sequence", "arrival_time", "departure_time"]]
stop_times = stop_times.sort_values(by=["trip_id", "stop_sequence"]).groupby("trip_id")

first_stops = stop_times.first().reset_index()
last_stops = stop_times.last().reset_index()
trip_stop_times = pd.merge(first_stops[["trip_id", "arrival_time"]], last_stops[["trip_id", "departure_time"]], on="trip_id")

schedule = schedule.merge(trip_stop_times, how="left", on="trip_id")
schedule = schedule.reindex(columns=["block_id", "trip_id", "departure_time", "arrival_time", "shape_id"]) #Reorder columns

# Add distance traveled
distances = distCalc.distance_traveled("shapes.txt")
schedule = schedule.merge(distances, on="shape_id")
schedule = schedule.drop(columns="shape_id")

schedule = schedule.sort_values(by=["block_id", "arrival_time"])

# Calculate bus statistics
schedule["arrival_time"] = pd.to_timedelta(schedule["arrival_time"])
schedule["departure_time"] = pd.to_timedelta(schedule["departure_time"])

schedule = schedule.groupby("block_id", sort = False)
bus_distances = schedule["Trip distance (in miles)"].sum().reset_index()

bus_times = schedule.agg(first_arrival = ("arrival_time","min"), last_departure = ("departure_time", "max"))
bus_times["Travel time (in hours)"] = (bus_times["last_departure"] - bus_times["first_arrival"]).dt.total_seconds()/3600
bus_times = bus_times.reset_index()

def num_Stops(group): # Daily stops per bus
    sum = 0
    for trip_id in group:
        sum+= len(stop_times.get_group(trip_id))
    return sum

bus_stops = schedule["trip_id"].apply(num_Stops).reset_index()
bus_stops.rename(columns = {"trip_id":"total stops"}, inplace = True)

bus_info = bus_distances.merge(bus_times[["Travel time (in hours)","block_id"]], on = "block_id").merge(bus_stops, on = "block_id")

# Displaying tables
print("=== Sample Bus Schedules ===") # Shows first 3 buses
count = 0
for key, group in schedule:
    count+=1
    print(group,"\n\n")
    if count>2:
        break

num_buses = len(bus_info)
print("=== Sample Bus Statistics ===\nTotal buses: ", num_buses) # Shows first and last 5
print(bus_info)

# Trip distance histogram
num_bins = (int)(num_buses**.5)
f, ax = plt.subplots(1,1,figsize=(14,9))
sns.histplot(bus_info["Trip distance (in miles)"], bins = num_bins, color = "#009391")
plt.tick_params(axis = "both", labelsize = 15)
plt.xlabel("Trip distance (in miles)", fontsize = 30)
plt.ylabel("Number of buses", fontsize = 30)
plt.title("Distribution of Trip Distances (Miles)", fontsize = 40)

# Travel time histogram
f, ax = plt.subplots(1,1,figsize=(14,9))
sns.histplot(bus_times["Travel time (in hours)"], bins = num_bins, color = "#009391")
plt.tick_params(axis = "both", labelsize = 15)
plt.xlabel("Travel time (in hours)", fontsize = 30)
plt.ylabel("Number of buses", fontsize = 30)
plt.title("Distribution of Travel Lengths (Hours)", fontsize = 40)
plt.show()

# Saving to CSV
if save_bus_schedule:
    schedule.to_csv(data_path / "bus_schedules.csv", index=False)  #Bus schedule by group
if save_bus_stats:
    bus_info.to_csv(data_path / "bus_stats.csv", index=False)      #Bus statistics