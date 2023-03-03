from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
import uvicorn
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def makeRequestURL(code: str) -> str:
  return f'https://wmata.esmel.workers.dev/backend/station/{code}'

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

app.mount("/static", StaticFiles(directory='static'), name="static")

def getCityFromStationName(station_name: str) -> str:
  with open('stations.json', 'r') as f:
    id_file = json.load(f)['cities']
    return id_file[station_name]

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
  return templates.TemplateResponse("credits.html", {"request": request})


@app.get('/search', response_class=HTMLResponse)
async def search(request: Request):
  return templates.TemplateResponse("search.html", {"request": request})


@app.get('/test', response_class=HTMLResponse)
async def test(request: Request):
  return templates.TemplateResponse("test.html", {"request": request})


@app.get('/station/', response_class=RedirectResponse)
async def station():
  return "/search"


@app.get('/info', response_class=HTMLResponse)
async def info(request: Request):
  return templates.TemplateResponse("info.html", {"request": request})


@app.get('/main.py')
async def main():
  return RedirectResponse(url="/")


@app.get('/hello', response_class=PlainTextResponse)
async def hello():
  return 'Hey there!'

@app.get('/creditsv2')
async def crd():
  return templates.TemplateResponse("creditsv2.html")


@app.get('/station/{name}', response_class=HTMLResponse)
async def makeStationHTML(request: Request, name: str):
  try:
    code = getIdFromStationName(name)

    city = getCityFromStationName(name)
    rq = requests.get(makeRequestURL(code))
    raw = rq.text

    return templates.TemplateResponse(
      'station.html', {
        "request": request,
        "station": name.replace("~", "/"),
        "city": city,
        "station_code": code,
        "data_raw": raw,
        "station_id": code
      })
  except KeyError:
    return RedirectResponse("/search")

uvicorn.run(app, host="0.0.0.0", port=80)