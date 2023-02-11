from flask import Flask, render_template, redirect #, after_request
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
    0: "No Data",
    1: "Not Crowded",
    2: "Somewhat Crowded",
    3: "Full"
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
# FlaskJSON(app)
app.config["JSON_ADD_STATUS"] = False

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/', methods=['GET'])
def index():
    return render_template("credits.html")

@app.route('/search', methods=['GET'])
def search():
  return render_template("search.html")

@app.route('/test', methods=['GET'])
def test():
  return render_template("test.html")

@app.route('/station/')
def station():
  return redirect("/search")

@app.route('/info', methods=['GET'])
def info():
  return render_template("info.html")

@app.route('/main.py')
def main():
  return 'Eww, Python... We use Rust, don\'t worry...'

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
       
        return render_template('station.html', station=name.replace("~", "/"), city=city, station_code=code, data_raw=raw, station_id=code)
    except KeyError:
        # return render_template('station.html', station="Whoops! That Station Doesn't Exist", station_code=":/")
          return redirect("/search")
      
# TODO: Add error handling
@app.route('/backend/station/<string:code>')
def backendDataGather(code):
    return requests.get(makeRequestURL(code)).text


app.run(host='0.0.0.0', port=443)
 