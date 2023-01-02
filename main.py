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
    station_json = rq.json()["TRAINS"]
    raw = rq.text

    
    train1 = station_json[0]
    line1 = train1['Line']
    dest1 = train1['Destination']
    time1 = train1['Min']
    unit1 = formatUnits(time1)
    cars1 = train1['Car']
    occu1 = train1['Oc']

    try:
      a = 1
      while station_json[a]['Group'] <= station_json[0]['Group'] + 0:
        a += 1
    except IndexError:
      a = 1
      while station_json[a]['Group'] == station_json[0]['Group']:
        a += 1
    train2 = station_json[a]
    line2 = train2['Line']
    dest2 = train2['Destination']
    time2 = train2['Min']
    unit2 = formatUnits(time2)
    cars2 = train2['Car']
    occu2 = train2['Oc']

    try:
      b = a + 1
      while station_json[b]['Group'] <= station_json[a]['Group'] + 1:
        b += 1
    except IndexError:
      try: 
        b = a + 1
        while station_json[b]['Group'] == station_json[a]['Group']:
          b += 1
      except IndexError:
        b = a
    train3 = station_json[b]
    line3 = train3['Line']
    dest3 = train3['Destination']
    time3 = train3['Min']
    unit3 = formatUnits(time3)
    cars3 = train3['Car']
    occu3 = train3['Oc']
    
    return render_template('station.html', station=name, city=city, station_code=code, line1=line1+".svg", dest1=dest1, time1=time1, unit1=unit1, cars1=cars1, occu1=OCCU_MAP_STR[occu1], line2=line2+".svg", dest2=dest2, time2=time2, unit2=unit2, cars2=cars2, occu2=OCCU_MAP_STR[occu2], line3=line3+".svg", dest3=dest3, time3=time3, unit3=unit3, cars3=cars3, occu3=OCCU_MAP_STR[occu3], data_raw=raw)
  except KeyError:
    return render_template('station.html', station="This Station Doesn't Exist", station_code=":/", line1="SAD.svg", dest1="Whoville", time1="Later?", cars1="i", occu1="idk", line2="SAD.svg")

@app.route('/backend/station/<string:code>')
def backendDataGather(code):
  pass


app.run(host='0.0.0.0', port=81)
