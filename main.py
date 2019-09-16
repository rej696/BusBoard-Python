import requests
import json


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
    def __init__(self, bus_stop_name, buses):
        self.bus_stop_name = bus_stop_name
        self.buses = buses

    @staticmethod
    def json_decoder(json_file):
        bus_stop_name = json_file["stop_name"]
        bus_departures_data = json_file["departures"]["all"]
        departures = []
        single_departure = SingleDeparture
        for index in range(len(bus_departures_data)):
            departures.append(single_departure.json_decoder(bus_departures_data[index]))
        return BusDepartures(bus_stop_name, departures)

    def __repr__(self):
        buses_string = [f"\nBus Stop Name : {self.bus_stop_name}\n"]
        for bus in self.buses:
            buses_string.append(str(bus))
        return "".join(buses_string)


def postcode_coordinates_api(postcode):
    postcode_info_json = requests.get("http://api.postcodes.io/postcodes/" + str(postcode)).json()
    return [postcode_info_json["result"]["longitude"], postcode_info_json["result"]["latitude"]]


def api_config():
    app_config = []
    with open("app_id.txt", "r") as file:
        app_config.append(file.read())
    with open("app_key.txt", "r") as file:
        app_config.append(file.read())
    return app_config


def identify_bus_stop(postcode):
    app_config = api_config()
    coordinates = postcode_coordinates_api(postcode)
    atcocode_json = requests.get(
        f"http://transportapi.com/v3/uk/places.json?"
        f"app_id={app_config[0]}"
        f"&app_key={app_config[1]}"
        f"&lat={coordinates[1]}"
        f"&lon={coordinates[0]}"
        f"&type=bus_stop"
    ).json()
    # distance_to_bus_stop = 7742
    # index = 0
    # counter = 0
    # for bus_stop in atcocode_json["member"]:
    #     if bus_stop["distance"] < distance_to_bus_stop:
    #         distance_to_bus_stop = bus_stop["distance"]
    #         index = counter
    #     counter += 1
    atcocode_lst = [atcocode_json["member"][0]["atcocode"], atcocode_json["member"][1]["atcocode"]]
    # atcocode = "0180BAA01336"  # Kelston View (The Hollow)
    # atcocode = "0180BAC30302"  # Lorne Road
    return atcocode_lst


def bus_stop_live_departures(atcocode, number_of_buses):
    app_config = api_config()
    bus_stop_data_json = requests.get(
        f"https://transportapi.com/v3/uk/bus/stop/{atcocode}"  # atcocode
        f"/live.json?app_id={app_config[0]}"  # app_id
        f"&app_key={app_config[1]}" # app_key
        f"&group=no" # group departures by route ("route") or return one group ("no")w
        f"&limit={number_of_buses}" +  # number of departures
        f"&nextbuses=no"
    ).json()
    return BusDepartures.json_decoder(bus_stop_data_json)


def main():
    print("Welcome to BusBoard.")
    postcode = str(input("Please enter your postcode: \n"))
    atcocode = identify_bus_stop(postcode)
    number_of_buses = input("How many buses would you like to see?: \n")
    bus_departures_1 = bus_stop_live_departures(atcocode[0], number_of_buses)
    print(bus_departures_1)
    bus_departures_2 = bus_stop_live_departures(atcocode[1], number_of_buses)
    print(bus_departures_2)

if __name__ == "__main__": main()