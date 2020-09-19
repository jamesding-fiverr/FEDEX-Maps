import json
import requests

with open('config.json') as configuration: #Read JSON from config.json
    config = json.loads(configuration.read())

def main():
    try:
        total_stops = int(input("Enter the total number of stops:\n"))
    except ValueError:
        print('Not a Valid Number.')
        return
    #Ask for first Stop
    starting_address = input("Enter the Starting Address:\n")
    stops_unsorted = [] #List of stops
    for i in range(total_stops):
        stop = input("Enter Address Number {}: ".format(i+1))
        api_return = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=formatted_address&key={}'.format(stop, config["google_api_key"])).json()
        if api_return["status"] == "OK":
            stops_unsorted.append(api_return["candidates"][0]["formatted_address"])
            print(api_return["candidates"][0]["formatted_address"] + " has successfully been added to the manifest")
        else:
            print(api_return["status"])
    stop_sorted = [] #List of Sorted Stops
    #Find First Nearest Stop from Starting Location
    distance_data = {}
    for stop in stops_unsorted:
        api_return = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units={}&origins={}&destinations={}&key={}'.format(config["units"], starting_address, stop, config["google_api_key"])).json()
        distance = api_return["rows"][0]["elements"][0]["distance"]["value"]
        distance_data[distance] = stop
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
    #Print Out Stops
    print("Stop Order:")
    for stop in stop_sorted:
        print(stop)
        
#Execute
main()