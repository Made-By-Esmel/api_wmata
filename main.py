from flask import Flask, render_template
import time
import json
import requests

def makeRequestURL(code: str) -> str:
    return f'https://www.wmata.com/components/stations.cfc?method=getNextTrains&StationCode={code}&returnFormat=JSON&_={int(time.time())}'

def formatUnits(mins) -> str:
    if type(mins) == int:
        return "MIN"
    return ""

OCCU_MAP_STR = {
    0: "Free",
    1: "Busy",
    2: "Full"
}

def getIdFromStationName(station_name: str) -> str:
    with open('stations.json', 'r') as f:
        id_file = json.load(f)['stations']
        return id_file[station_name]

def getCityFromStationName(station_name: str) -> str:
    with open('stations.json', 'r') as f:
        id_file = json.load(f)['cities']
        return id_file[station_name]

app = Flask(__name__)
FlaskJSON(app)
app.config["JSON_ADD_STATUS"] = False


@app.route('/', methods=['GET'])
def index():
    return render_template("credits.html")


@app.route('/hello')
def hello():
    return 'Hey there!'

@app.route('/station/<string:name>')
def makeStationHTML(name):
    try:
        code = getIdFromStationName(name)
        city = getCityFromStationName(name)
        rq = requests.get(makeRequestURL(code))
        # station_json = rq.json()["TRAINS"]
        raw = rq.text
        return render_template('station.html', station=name, city=city, station_code=code, data_raw=raw)
    except KeyError:
        return render_template('station.html', station="This Station Doesn't Exist", station_code=":/")

# TODO: Add error handling
@app.route('/backend/station/<string:code>')
def backendDataGather(code):
    return requests.get(makeRequestURL(code)).text


app.run(host='0.0.0.0', port=81)
