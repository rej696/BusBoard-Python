from flask import Flask, render_template, request
from main import PostcodeAPI, TransportAPI

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/busInfo")
def busInfo():
    postcode_string = request.args.get('postcode')
    postcodeApi = PostcodeAPI()
    transportApi = TransportAPI()

    postcode = postcodeApi.get_postcode(postcode_string)
    if postcode == None:
        return render_template('info.html', postcode="Bad postcode: " + postcode_string, stops=[])
    stopcodes = transportApi.get_stopcodes_nearest(postcode.latitude(), postcode.longitude())
    stops = [transportApi.get_live_bus_stop(stopcode) for stopcode in stopcodes[0:2]]

    return render_template('info.html', postcode=postcode.name(), stops=stops)

if __name__ == "__main__": app.run()