import requests
import json

def get_application_keys():
    with open('secrets.txt') as f:
        data = f.read().split("\n")
    # Either substitute your API keys here or write a secrets.txt file with the ID in the first line and key in the second
    return {'app_id': data[0], 'app_key': data[1]}

class TransportAPI:
    def __init__(self):
        api_keys = get_application_keys()
        self.payload = api_keys

    def get_stopcodes_nearest(self, latitude, longitude):
        stops_data_response = requests.get(f'http://transportapi.com/v3/uk/places.json?lat={latitude}&lon={longitude}&type=bus_stop', params=self.payload)
        stops_data = json.loads(stops_data_response.text)
        nearest_stopcodes = [stop['atcocode'] for stop in stops_data['member']]
        return nearest_stopcodes

    def get_live_bus_stop(self, atcocode):
        stop_data_response = requests.get(f'http://transportapi.com/v3/uk/bus/stop/{atcocode}/live.json', params=self.payload)
        stop_data = json.loads(stop_data_response.text)
        stop = LiveBusStop(stop_data)
        return stop

class LiveBusStop:
    def __init__(self, data):
        self.data = data
        self.buses = [Bus(bus_data) for line in data['departures'] for bus_data in data['departures'][line]]
    
    def name(self):
        return self.data['name']

    def next_departures(self):
        self.buses.sort(key=lambda b: b.departs())
        return "\n".join([bus.to_string() for bus in self.buses[0:5]])

class Bus:
    def __init__(self, data):
        self.data = data
    
    def line_name(self):
        return self.data['line_name']
    
    def departs(self):
        return self.data['best_departure_estimate']
    
    def to_string(self):
        return f"{self.departs()} - {self.line_name()}"

class PostcodeAPI:
    def get_postcode(self, postcode):
        postcode_data_response = requests.get(f'http://api.postcodes.io/postcodes/{postcode}')
        postcode_data = json.loads(postcode_data_response.text)
        if postcode_data['status'] != 200:
            return None
        postcode = Postcode(postcode_data)
        return postcode

class Postcode:
    def __init__(self, data):
        self.data = data['result']
    
    def longitude(self):
        return self.data['longitude']

    def latitude(self):
        return self.data['latitude']

def main():
    postcodeApi = PostcodeAPI()
    transportApi = TransportAPI()

    print('Welcome to BusBoard.')
    postcode_string = input('Please input a postcode: ')
    postcode = postcodeApi.get_postcode(postcode_string)
    if postcode == None:
        print("Bad postcode.")
        return
    stopcodes = transportApi.get_stopcodes_nearest(postcode.latitude(), postcode.longitude())

    for stopcode in stopcodes[0:2]:
        stop = transportApi.get_live_bus_stop(stopcode)        
        print('These are the upcoming buses at ' + stop.name() + ':')
        print(stop.next_departures())
        print()

if __name__ == "__main__": main()