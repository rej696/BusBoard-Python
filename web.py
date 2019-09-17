from flask import Flask, render_template, request
from classes import PostcodeTravelInfo

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/busInfo")
def bus_info():
    postcode = request.args.get('postcode')
    number_of_stops = request.args.get('number_of_stops')
    number_of_buses = request.args.get('number_of_buses')
    postcode_travel_info = PostcodeTravelInfo(postcode, number_of_stops, number_of_buses)
    line_name = postcode_travel_info.bus_stops[0].departures[0].line_name
    return render_template(
        'info.html', postcode=postcode, number_of_stops=number_of_stops, number_of_buses=number_of_buses,
        line_name=line_name
    )


if __name__ == "__main__": app.run()