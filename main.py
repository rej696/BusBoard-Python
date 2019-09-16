import requests

def main():
    print("Welcome to BusBoard.")
    # atcocode = input("Please enter a bus stop code: \n")
    atcocode = "0180BAC30592"
    with open("app_id.txt", "r") as file:
        app_id = file.read()
    with open("app_key.txt", "r") as file:
        app_key = file.read()
    r = requests.get(
        "https://transportapi.com/v3/uk/bus/stop/"
        + atcocode +  # atcocode
        "/live.json?app_id=" + app_id +  # app_id
        "&app_key=" + app_key +  # app_key
        "&group=" + "route" +  # group departures by route ("route") or return one group ("no")w
        "&integer=" + "5" +  # number of departures
        "&nextbuses=" + "yes"
    )
    json_file = r.json()
    print(json_file)



if __name__ == "__main__": main()