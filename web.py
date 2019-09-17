from flask import Flask, render_template, request
from main import BusDepartures
from main import SingleDeparture
from main import TransportApi

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/busInfo")
def busInfo():
    postcode = request.args.get('postcode')
    return render_template('info.html', postcode=postcode)
    print("Welcome to BusBoard.")
    cont = True
    while cont:
        postcode = str(input("Please enter your postcode: \n"))
        transport_api = TransportApi(postcode)
        number_of_stops = int(input("How many bus stops would you like to see?: \n"))
        atcocode_lst = transport_api.identify_bus_stop(number_of_stops)
        number_of_buses = input("How many buses would you like to see?: \n")
        for atcocode in atcocode_lst:
            bus_departures = transport_api.bus_stop_live_departures(atcocode, number_of_buses)
            if bus_departures is not None:
                cont = False
                print(bus_departures)

if __name__ == "__main__": app.run()