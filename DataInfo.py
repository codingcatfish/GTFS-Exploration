#Prints out sample rows from each file and explains what each column means
import pandas as pd
from pathlib import Path

pd.set_option('display.width',1000)
pd.set_option('display.max_columns',20)

#Set data_path to the location of the GTFS folder containing routes.txt, trips.txt, etc.
data_path = Path.cwd() / "GTFSData"

def print_data(file_path):
    data = pd.read_csv(data_path / file_path)
    print(data.head())


print("==== ROUTE DATA ====")
print_data("routes.txt")
print("\nroute_id: This route's unique ID\nagency_id: The agency of the route\nroute_short_name: Short name riders use to identify the route\nroute_long_name: A more descriptive full route name\nroute_desc: Describes the route, usually with its operating endpoints\nroute_type: Type of transportation (Values 0-12, 3 = Bus route)\nroute_color: Route color designation\nroute_text_color: Color to use for legible text on top of route_color\n\n\n")


print("==== TRIP DATA ====")
print_data("trips.txt")
print("\nroute_id: The route this trip is part of\nservice_id: Dates when service is available for routes\ntrip_id: This trip's unique ID\ntrip_headsign: Text that describes the trip for riders\ndirection_id: Direction of travel for a trip (0 = traveling in one direction, 1 = traveling in the opposite direction)\nblock_id: The block this trip is part of (Block = Trips made with the same vehicle)\nshape_id: ID of the shape that describes this trip\n\n\n")


print("==== STOP DATA ====")
print_data("stops.txt")
print("\nstop_id: This stop's unique ID\nstop_name: Name of the stop location\nstop_desc: Description of the location\nstop_lat: Latitude of the location\nstop_lon: Longitude of the location\nzone_id: The fare zone for the stop\nstop_url: URL link to a web page about the location\nlocation_type: Describes the stop type (Values 0-4, 0 = default and describes a Stop or Platform)\nparent_station: ID of a parent location in the stop data, if applicable\n\n\n")


print("==== STOP TIME DATA ====")
print_data("stop_times.txt")
print("\ntrip_id: The trip these stop times belong to\narrival_time: Arrival time at stop\ndeparture_time: Departure time from stop\nstop_id: ID of the stop described\nstop_sequence: Ordering of the stop (trip progresses with increasing stop sequence)\npickup_type: Pickup method (Values 0-3, 0 = regularly scheduled)\ndrop_off_type: Drop off method (Values 0-3, 0 = regularly scheduled)\ntimepoint: If arrival and departure times are exact (0 = approximate, 1 = exact)\n\n\n")


print("==== SHAPE DATA ====")
print_data("shapes.txt")
print("*Every row represents one shape point\nshape_id: This shape's unique ID\nshape_pt_lat: The latitude of this shape point\nshape_pt:lon: The longitude of this shape point\nshape_pt_seq: Ordering of this shape point (Shape is connected by connecting points in increasing order)")