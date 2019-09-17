from flask import Flask, render_template, request
from classes import BusDepartures
from classes import SingleDeparture
from classes import TransportApi
from classes import PostcodeTravelInfo

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/busInfo")
def busInfo():
    postcode = request.args.get('postcode')
    foo = BusDepartures().bus_stop_name
    return render_template('info.html', postcode=postcode, bar=foo)

if __name__ == "__main__": app.run()