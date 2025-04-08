import requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import calendar
from collections import defaultdict
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

API_KEY = "22cf61ec3c1f44665e6140df5891c249"  

@app.post("/weather", response_class=HTMLResponse)
async def get_weather(request: Request, city: str = Form(...)):
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=cz"
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=cz"

    weather_response = requests.get(weather_url).json()
    forecast_response = requests.get(forecast_url).json()

    now = datetime.now()
    today = now.date()

    # Data pro grafy
    todays_data = [
        item for item in forecast_response["list"]
        if datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S").date() == today
    ]
    if not todays_data:
        todays_data = forecast_response["list"][:8]

    labels = [item["dt_txt"][11:16] for item in todays_data]
    temperatures = [item["main"]["temp"] for item in todays_data]
    rain_data = [item.get("rain", {}).get("3h", 0) for item in todays_data]

    # Rozdělení dat podle dnů (bez dneška)
    forecast_by_day = defaultdict(list)
    for item in forecast_response["list"]:
        dt = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
        if dt.date() == today:
            continue
        day_name = calendar.day_name[dt.weekday()]
        forecast_by_day[day_name].append({
            "time": dt.strftime("%H:%M"),
            "temp": item["main"]["temp"],
            "description": item["weather"][0]["description"],
            "icon": item["weather"][0]["icon"],
            "humidity": item["main"]["humidity"],
            "wind": item["wind"]["speed"]
        })

    # Zachování pořadí dnů
    ordered_days = []
    seen = set()
    for item in forecast_response["list"]:
        dt = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
        day = calendar.day_name[dt.weekday()]
        if dt.date() != today and day not in seen:
            ordered_days.append(day)
            seen.add(day)

    # Výběr obrázku na pozadí
    condition = weather_response["weather"][0]["main"].lower()
    backgrounds = {
        "clear": "sun.jpg",
        "clouds": "clouds.jpg",
        "rain": "rain.jpg",
        "snow": "snow.jpg",
        "thunderstorm": "storm.jpg",
        "drizzle": "rain.jpg",
        "mist": "fog.jpg"
    }
    background_image = f"/static/img/{backgrounds.get(condition, 'sun.jpg')}"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "weather": weather_response,
        "labels": labels,
        "temperatures": temperatures,
        "rain_data": rain_data,
        "forecast_by_day": forecast_by_day,
        "ordered_days": ordered_days,
        "city": city,
        "background_image": background_image
    })

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
