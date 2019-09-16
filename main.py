import requests
import json


def departures_json_decoder(bus_data_json):
    bus_data_all = bus_data_json.json()
    bus_data = bus_data_all["departures"]["all"]
    departures_dict = []
    for index in range(len(bus_data)):
        departures_dict.append({
            "Line Name": bus_data[index]["line_name"],
            "Aimed Departure Time": bus_data[index]["aimed_departure_time"],
            "Expected Departure Time": bus_data[index]["best_departure_estimate"],
            "Final Destination": bus_data[index]["direction"]
        })
    return departures_dict


def bus_stop_json_decoder(bus_data_json):
    bus_data_all = bus_data_json.json()
    bus_stop_data = {
        "Stop Name": bus_data_all["stop_name"],
    }
    return bus_stop_data


def display_bus_data(bus_data):
    for key in bus_data:
        print(key + ": ", bus_data[key])


def main():
    print("Welcome to BusBoard.")
    # atcocode = input("Please enter a bus stop code: \n")
    atcocode = "0180BAA01336"  # Kelston View (The Hollow)
    # atcocode = "0180BAC30302"  # Lorne Road
    with open("app_id.txt", "r") as file:
        app_id = file.read()
    with open("app_key.txt", "r") as file:
        app_key = file.read()
    bus_data_json = requests.get(
        "https://transportapi.com/v3/uk/bus/stop/"
        + atcocode +  # atcocode
        "/live.json?app_id=" + app_id +  # app_id
        "&app_key=" + app_key +  # app_key
        "&group=" + "no" +  # group departures by route ("route") or return one group ("no")w
        "&limit=" + "5" +  # number of departures
        "&nextbuses=" + "no"
    )
    # with open("bus_data.json", "r") as file:
    #     bus_data_json = file.read()
    bus_stop_data_decoded = bus_stop_json_decoder(bus_data_json)
    display_bus_data(bus_stop_data_decoded)
    departures_dict = departures_json_decoder(bus_data_json)
    for index in range(len(departures_dict)):
        print("\nBus Number " + str(index + 1))
        display_bus_data(departures_dict[index])


if __name__ == "__main__": main()