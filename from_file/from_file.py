import json
import requests

with open('./config.json') as configuration: #Read JSON from config.json
    config = json.loads(configuration.read())



def main():
    #Ask for first Stop
    starting_address = input("Enter the Starting Address:\n")
    stops_unsorted = open('./from_file/file.txt').read().splitlines()
    total_stops = len(stops_unsorted)
    stop_sorted = [] #List of Sorted Stops
    #Find First Nearest Stop from Starting Location
    distance_data = {}
    print("Stops: {}\nTotal Stops: {}".format(", ".join(stops_unsorted), len(stops_unsorted)))
    for stop in stops_unsorted:
        api_return = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units={}&origins={}&destinations={}&key={}'.format(config["units"], starting_address, stop, config["google_api_key"])).json()
        if api_return["status"] == "OK":
            distance = api_return["rows"][0]["elements"][0]["distance"]["value"]
            distance_data[distance] = stop
        else:
            print("{} not found.".format(stop))
    first_stop = distance_data[min(distance_data.keys())]
    stop_sorted.append(first_stop)
    stops_unsorted.remove(first_stop)
    for i in range(total_stops-1):
        distance_data = {}
        for stop in stops_unsorted:
            previous_address = stop_sorted[-1]
            api_return = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units={}&origins={}&destinations={}&key={}'.format(config["units"], previous_address, stop, config["google_api_key"])).json()
            distance = api_return["rows"][0]["elements"][0]["distance"]["value"]
            distance_data[distance] = stop
        next_stop = distance_data[min(distance_data.keys())]
        stop_sorted.append(next_stop)
        stops_unsorted.remove(next_stop)
        print("Stop No. {}: {}".format(i+1, next_stop))
    #Print Out Stops
        
#Execute
main()