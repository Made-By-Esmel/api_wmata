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


@app.route('/', methods=['GET'])
def index():
    return render_template("credits.html")

@app.route('/search', methods=['GET'])
def search():
  return render_template("search.html")

@app.route('/test', methods=['GET'])
def test():
  return render_template("test.html")

@app.route('/hello')
def hello():
    return 'Hey there!'

@app.route('/suggestions.json')
def suggestions():
    return '["Addison Road-Seat Pleasant","Anacostia","Archives-Navy Memorial-Penn Quarter","Arlington Cemetery","Ashburn","Ballston-MU","Benning Road","Bethesda","Braddock Road","Branch Ave","Brookland-CUA","Capitol Heights","Capitol South","Cheverly","Clarendon","Cleveland Park","College Park-U of Md","Columbia Heights","Congress Heights","Court House","Crystal City","Deanwood","Downtown Largo","Dunn Loring-Merrifield","Dupont Circle","East Falls Church","Eastern Market","Eisenhower Avenue","Farragut North","Farragut West","Federal Center SW","Federal Triangle","Foggy Bottom-GWU","Forest Glen","Fort Totten","Franconia-Springfield","Friendship Heights","Gallery Pl-Chinatown","Georgia Ave-Petworth","Glenmont","Greenbelt","Greensboro","Grosvenor-Strathmore","Herndon","Huntington","Hyattsville Crossing","Innovation Center","Judiciary Square","King St-Old Town","L\'Enfant Plaza","Landover","Loudoun Gateway","McLean","McPherson Square","Medical Center","Metro Center","Minnesota Ave","Morgan Boulevard","Mt Vernon Sq 7th St-Convention Center","Navy Yard-Ballpark","Naylor Road","New Carrollton","NoMa-Gallaudet U","North Bethesda","Pentagon","Pentagon City","Potomac Ave","Reston Town Center","Rhode Island Ave-Brentwood","Rockville","Ronald Reagan Washington National Airport","Rosslyn","Shady Grove","Shaw-Howard U","Silver Spring","Silver Spring Transit Center","Smithsonian","Southern Avenue","Spring Hill","Stadium-Armory","Suitland","Takoma","Tenleytown-AU","Twinbrook","Tysons","U Street/African-Amer Civil War Memorial/Cardozo","Union Station","Van Dorn Street","Van Ness-UDC","Vienna/Fairfax-GMU","Virginia Square-GMU","Washington Dulles International Airport","Waterfront","West Falls Church","West Hyattsville","Wheaton","Wiehle-Reston East","Woodley Park-Zoo/Adams Morgan" ]'

@app.route('/station/<string:name>')
def makeStationHTML(name):
    try:
        code = getIdFromStationName(name)
        city = getCityFromStationName(name)
        rq = requests.get(makeRequestURL(code))
        # station_json = rq.json()["TRAINS"]
        raw = rq.text
        return render_template('station.html', station=name, city=city, station_code=code, data_raw=raw, station_id=code)
    except KeyError:
        return render_template('station.html', station="Whoops! That Station Doesn't Exist", station_code=":/")

# TODO: Add error handling
@app.route('/backend/station/<string:code>')
def backendDataGather(code):
    return requests.get(makeRequestURL(code)).text


app.run(host='0.0.0.0', port=81)
