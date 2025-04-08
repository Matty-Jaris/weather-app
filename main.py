from datetime import datetime, date
import httpx
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from collections import defaultdict
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")

API_KEY = "22cf61ec3c1f44665e6140df5891c249"

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Funkce pro získání aktuálního počasí
async def get_weather(city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=cz"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("message"))
        weather_data = response.json()
        return weather_data, None

# Funkce pro získání předpovědi na 5 dní (3hodinově)
async def get_forecast_5days(city: str):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=cz"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("message"))
        return response.json()
# Funkce pro získání dat pro dnešní den pro graf
def extract_today_forecast(forecast_data):
    today = date.today()
    today_data = [
        entry for entry in forecast_data["list"]
        if datetime.fromisoformat(entry["dt_txt"]).date() == today
    ]
    return today_data

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/weather", response_class=HTMLResponse)
async def weather(request: Request, city: str):
    weather_data, _ = await get_weather(city)
    forecast_data = await get_forecast_5days(city)
    today_forecast = extract_today_forecast(forecast_data)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "weather": weather_data,
        "forecast": forecast_data,
        "today_forecast": today_forecast
    })
