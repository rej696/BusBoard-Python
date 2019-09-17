from flask import Flask, render_template, request
from classes import PostcodeTravelInfo

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/busInfo")
def BusInfo():
    postcode = request.args.get('postcode')
    number_of_stops = int(request.args.get('number_of_stops'))
    number_of_buses = request.args.get('number_of_buses')
    postcode_travel_info = PostcodeTravelInfo(postcode, number_of_stops, number_of_buses)
    return render_template(
        'info.html', postcode=postcode, number_of_stops=number_of_stops, number_of_buses=number_of_buses,
        postcode_travel_info=postcode_travel_info
    )


if __name__ == "__main__": app.run()