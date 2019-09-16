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


def main():
    print("Welcome to BusBoard.")
    # atcocode = input("Please enter a bus stop code: \n")
    atcocode = "0180BAA01336"  # Kelston View (The Hollow)
    # atcocode = "0180BAC30302"  # Lorne Road
    with open("app_id.txt", "r") as file:
        app_id = file.read()
    with open("app_key.txt", "r") as file:
        app_key = file.read()
    bus_stop_data_json = requests.get(
        "https://transportapi.com/v3/uk/bus/stop/"
        + atcocode +  # atcocode
        "/live.json?app_id=" + app_id +  # app_id
        "&app_key=" + app_key +  # app_key
        "&group=" + "no" +  # group departures by route ("route") or return one group ("no")w
        "&limit=" + "5" +  # number of departures
        "&nextbuses=" + "no"
    ).json()
    bus_departures = BusDepartures.json_decoder(bus_stop_data_json)
    print(bus_departures)


if __name__ == "__main__": main()