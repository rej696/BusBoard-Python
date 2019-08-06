import requests
import json

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

def get_application_keys():
    with open('secrets.txt') as f:
        data = f.read().split("\n")
    # Either substitute your API keys here or write a secrets.txt file with the ID in the first line and key in the second
    return {'app_id': data[0], 'app_key': data[1]}

def main():
    api_keys = get_application_keys()

    print('Welcome to BusBoard.')
    atcocode = input('Please input a stopcode: ')
    payload = api_keys
    stop_data_response = requests.get(f'http://transportapi.com/v3/uk/bus/stop/{atcocode}/live.json', params=payload)
    stop_data = json.loads(stop_data_response.text)
    stop = LiveBusStop(stop_data)

    print('These are the upcoming buses at ' + stop.name() + ':')
    print(stop.next_departures())

if __name__ == "__main__": main()