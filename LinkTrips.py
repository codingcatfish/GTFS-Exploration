#Builds a basic schedule showing which trips stop where and when.
import pandas as pd
import MS3TripDistance as distCalc
from pathlib import Path

pd.set_option('display.width',1000)
pd.set_option('display.max_columns',100)

data_path = Path.cwd() / "GTFSData"

def read_data(file_path):
    return pd.read_csv(data_path / file_path)

schedule = read_data("trips.txt")[["trip_id","route_id", "shape_id"]]
stop_times = read_data("stop_times.txt")[["trip_id","stop_sequence","stop_id","arrival_time","departure_time"]]
stops = read_data("stops.txt")[["stop_id","stop_name"]]

stop_times = stop_times.merge(stops, how = "left", on = "stop_id")
stop_times = stop_times.drop(columns = "stop_id")

schedule = schedule.merge(stop_times, how = "left", on = "trip_id")

schedule = schedule.reindex(columns = ["trip_id","route_id","stop_sequence","stop_name","arrival_time","departure_time","shape_id"])
schedule = schedule.sort_values(by=["departure_time"])

distances = distCalc.distance_traveled("shapes.txt")
schedule = schedule.merge(distances, how = "left", on = "shape_id")
schedule = schedule.drop(columns = "shape_id")
print(schedule)

#schedule.to_csv(data_path / "combined.txt")