import requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

API_KEY = "22cf61ec3c1f44665e6140df5891c249"

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/weather", response_class=HTMLResponse)
async def get_weather(request: Request, city: str = Form(...)):
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=cz"
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=cz"

    weather_response = requests.get(weather_url).json()
    forecast_response = requests.get(forecast_url).json()

    # Výpis do konzole pro kontrolu
    print(weather_response)
    print(forecast_response)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "weather": weather_response,
        "forecast": forecast_response
    })
