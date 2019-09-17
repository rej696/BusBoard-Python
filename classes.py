import requests
import logging
logging.basicConfig(filename="BusBoard.log", filemode="w", level=logging.DEBUG)


class SingleDeparture:
    def __init__(self, line_name, aimed_departure_time, expected_departure_time, final_destination):
        self.line_name = line_name
        self.aimed_departure_time = aimed_departure_time
        self.expected_departure_time = expected_departure_time
        self.final_destination = final_destination

    def __repr__(self):
        single_departure = f"\nLine Name : {self.line_name}\nAimed Departure Time : {self.aimed_departure_time}\n" \
                           f"Expected Departure Time : {self.expected_departure_time}\n" \
                           f"Final Destination : {self.final_destination}\n"
        return single_departure

    @staticmethod
    def json_decoder(single_bus_departure_json):
        return SingleDeparture(
            single_bus_departure_json["line_name"], single_bus_departure_json["aimed_departure_time"],
            single_bus_departure_json["best_departure_estimate"], single_bus_departure_json["direction"]
        )


class BusDepartures:
    def __init__(self, bus_stop_name, departures):
        self.bus_stop_name = bus_stop_name
        self.departures = departures

    @staticmethod
    def json_decoder(json_file):
        bus_stop_name = json_file["stop_name"]
        try:
            bus_departures_data = json_file["departures"]["all"]
        except KeyError:
            logging.info(
                f"key error raised, likely that the json for the stop {bus_stop_name} does not contain any departures"
            )
            print(f"No buses found at {bus_stop_name}")
            return None
        except:
            logging.info("an unknown error occurred with determining the departures from the json file")
            return None
        departures = []
        for index in range(len(bus_departures_data)):
            departures.append(SingleDeparture.json_decoder(bus_departures_data[index]))
        return BusDepartures(bus_stop_name, departures)

    def __repr__(self):
        buses_string = [f"\nBus Stop Name : {self.bus_stop_name}\n"]
        for bus in self.departures:
            buses_string.append(str(bus))
        return "".join(buses_string)


class TransportApi:
    def __init__(self, postcode):
        app_config = []
        with open("app_id.txt", "r") as file:
            app_config.append(file.read())
        with open("app_key.txt", "r") as file:
            app_config.append(file.read())
        self.app_config = app_config
        self.postcode = postcode

    def identify_bus_stop(self, number_of_stops):
        postcode_info_json = requests.get("http://api.postcodes.io/postcodes/" + str(self.postcode)).json()
        coordinates = [postcode_info_json["result"]["longitude"], postcode_info_json["result"]["latitude"]]
        atcocode_json = requests.get(
            f"http://transportapi.com/v3/uk/places.json?"
            f"app_id={self.app_config[0]}"
            f"&app_key={self.app_config[1]}"
            f"&lat={coordinates[1]}"
            f"&lon={coordinates[0]}"
            f"&type=bus_stop"
        ).json()
        atcocode_lst = []
        counter = 0
        for bus_stop in atcocode_json["member"]:
            if counter < number_of_stops:
                atcocode_lst.append(bus_stop["atcocode"])
            counter += 1
        return atcocode_lst

    def bus_stop_live_departures(self, atcocode, number_of_buses):
        bus_stop_data_json = requests.get(
            f"https://transportapi.com/v3/uk/bus/stop/{atcocode}"  # atcocode
            f"/live.json?app_id={self.app_config[0]}"
            f"&app_key={self.app_config[1]}"  # app_key
            f"&group=no"  # group departures by route ("route") or return one group ("no")w
            f"&limit={number_of_buses}"  # number of departures
            f"&nextbuses=no"
        ).json()
        return BusDepartures.json_decoder(bus_stop_data_json)


class PostcodeTravelInfo:
    def __init__(self, postcode, number_of_stops, number_of_buses):
        self.postcode = postcode
        self.number_of_stops = number_of_stops
        self.number_of_buses = number_of_buses
        transport_api = TransportApi(self.postcode)
        atcocode_lst = transport_api.identify_bus_stop(self.number_of_stops)
        bus_stops = []
        for atcocode in atcocode_lst:
            bus_stops.append(transport_api.bus_stop_live_departures(atcocode, self.number_of_buses))
        self.bus_stops = bus_stops

    def display(self):
        for index in range(self.number_of_stops):
            print(self.bus_stops[index])
