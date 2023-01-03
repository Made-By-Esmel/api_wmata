from flask import Flask, request, render_template
from flask_json import FlaskJSON, json_response
import hashlib
import time
import json
import requests

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
  #'Flask by Markian (GitHub: <a href="https://github.com/PlanMan1717/" target="_blank">@PlanMan1717</a>). Edits from Andrew (Portfolio: <a href="https://esmel.xyz/" target="_blank">@Esm&eacute;l</a>).'
  #'Made by Markian & Andrew Frykman in 2022'


@app.route('/hello')
def hello():
    return 'Hey there!'


# In the future, this should expect parameters
@app.route('/wmata/<string:code>', methods=['GET'])
def nextFiveLines(code):
    # print(request.args['station'])
    # code = request.get_json()['station']
    time_now = int(time.time())
    station_json = requests.get(
        f'https://www.wmata.com/components/stations.cfc?method=getNextTrains&StationCode={code}&returnFormat=JSON&_={time_now}'
    ).json()["TRAINS"]

    out_str = ''
  
    for train in station_json:
      train_string = str(train)
      train_string = train_string.replace("'Oc': 0", "'Oc': 'Not Crowded'")
      train_string = train_string.replace("'Oc': 1", "'Oc': 'Somewhat Crowded'")
      train_string = train_string.replace("'Oc': 2", "'Oc': 'Crowded'")
      

      out_str += train_string  
  
    return '''
  <style>
  p {
    /*background-color: black;*/
    color: white;
    font-size: 13px;
    font-family: monospace;
  }

  body {
    background-color: black;
  }
  </style>
  <p>''' + out_str + '</p>'

@app.route('/station/<string:name>')
def makeStationHTML(name):
  try:
    code = getIdFromStationName(name)
    city = getCityFromStationName(name)
    rq = requests.get(
        f'https://www.wmata.com/components/stations.cfc?method=getNextTrains&StationCode={code}&returnFormat=JSON&_={int(time.time())}'
    )
    # station_json = rq.json()["TRAINS"]
    raw = rq.text

    
    return render_template('station.html', station=name, city=city, station_code=code, data_raw=raw)
  except KeyError:
    return render_template('station.html', station="This Station Doesn't Exist", station_code=":/")

@app.route('/backend/station/<string:code>')
def backendDataGather(code):
  pass


app.run(host='0.0.0.0', port=81)
