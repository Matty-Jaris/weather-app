# ⛅️ Weather App – Forecast with Clarity

This app serves as a modern and responsive tool for checking current weather and forecasts. It's part of my personal digital portfolio and demonstrates the integration of a Python backend (FastAPI) with a modern Tailwind CSS frontend.

## ✨ Features

- Search for weather by city
- Display of current temperature, humidity, wind, pressure, etc.
- 5-day forecast in 3-hour intervals
- Graphs for temperature and precipitation for the current day
- Background or styling changes based on weather conditions
- Simple dashboard with weather records

## 🔧 Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/) – lightning-fast Python backend
- [OpenWeatherMap API](https://openweathermap.org/api) – weather data source
- [Jinja2](https://jinja.palletsprojects.com/) – templating engine
- [Tailwind CSS](https://tailwindcss.com/) – utility-first CSS framework
- [npm](https://www.npmjs.com/) – package manager for frontend dependencies
- (optional) [Chart.js](https://www.chartjs.org/) or `matplotlib` for rendering charts

## 🚀 Local Setup

1. Clone the repository:

```bash
git clone https://github.com/Matty-Jaris/weather-app.git
cd weather-app
```

2. Set up Python virtual environment and install dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Install frontend dependencies:

```bash
npm install
```

4. Build Tailwind CSS:

```bash
npx tailwindcss -i ./static/css/input.css -o ./static/css/tailwind.css --watch
```

5. Run the FastAPI server:

```bash
uvicorn main:app --reload
```

Visit the app at `http://127.0.0.1:8000`

## 📁 Project Structure

```
weather_app/
│
├── static/
│   └── css/
│       ├── input.css
│       └── tailwind.css (generated)
│
├── templates/
│   └── base.html
│   └── index.html
│
├── main.py
├── tailwind.config.js
├── postcss.config.js
├── package.json
└── .gitignore
```

## 🙋‍♂️ Author

**Martin Jarábek**\
A teacher transitioning into a programmer.\
[GitHub – Matty-Jaris](https://github.com/Matty-Jaris)

 

