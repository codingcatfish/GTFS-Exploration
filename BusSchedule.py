#Builds a basic schedule showing which trips stop where and when.
import pandas as pd
import MS3TripDistance as distCalc
from pathlib import Path

pd.set_option('display.width',1000)
pd.set_option('display.max_columns',100)

data_path = Path.cwd() / "GTFSData"

def read_data(file_path):
    return pd.read_csv(data_path / file_path)

schedule = read_data("trips.txt")[["trip_id", "block_id", "shape_id"]]

stop_times = read_data("stop_times.txt")[["trip_id", "stop_sequence", "arrival_time", "departure_time"]]
stop_times = stop_times.sort_values(by=["trip_id", "stop_sequence"]).groupby("trip_id")


first_stops = stop_times.first().reset_index()
last_stops = stop_times.last().reset_index()
trip_stop_times = pd.merge(first_stops[["trip_id", "arrival_time"]], last_stops[["trip_id", "departure_time"]], on="trip_id")

schedule = schedule.merge(trip_stop_times, how="left", on="trip_id")

#Reorder columns
schedule = schedule.reindex(columns=["block_id", "trip_id", "departure_time", "arrival_time", "shape_id"])

#Add distance traveled
distances = distCalc.distance_traveled("shapes.txt")
schedule = schedule.merge(distances, on="shape_id")
schedule = schedule.drop(columns="shape_id")

schedule = schedule.sort_values(by=["block_id", "arrival_time"])


#Bus statistics

schedule["arrival_time"] = pd.to_timedelta(schedule["arrival_time"])
schedule["departure_time"] = pd.to_timedelta(schedule["departure_time"])

schedule = schedule.groupby("block_id", sort = False)

bus_distances = schedule["Trip distance (in miles)"].sum().reset_index()

bus_times = schedule.agg(first_arrival = ("arrival_time","min"), last_departure = ("departure_time", "max"))
bus_times["Travel time (in hours)"] = (bus_times["last_departure"] - bus_times["first_arrival"])
bus_times = bus_times.reset_index()

def numStops(group):
    sum = 0
    for trip_id in group:
        sum+= len(stop_times.get_group(trip_id))
    return sum

bus_stops = schedule["trip_id"].apply(numStops).reset_index()
bus_stops.rename(columns = {"trip_id":"total stops"}, inplace = True)

bus_info = bus_distances.merge(bus_times[["Travel time (in hours)","block_id"]], on = "block_id").merge(bus_stops, on = "block_id")
print(bus_info)


#for key, item in schedule:
   # print(schedule.get_group(key),"\n\n")
#schedule.to_csv(data_path / "bus_schedules.csv", index=False)
#bus_info.to_csv(data_path / "bus_stats.csv", index=False)