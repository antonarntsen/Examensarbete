from flask import Flask, render_template, request
from waitress import serve
import requests
import sys

app = Flask(__name__)
key = str(sys.argv[1])
gray = "#474747"

def get_weather(api_key, city):
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key,
        "q": city,
        "aqi": "no"
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if 'error' in data:
        return None
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        api_key = "689649eb6e934beaa8591200230805"
        city = request.form['city']
        weather_data = get_weather(api_key, city)
        if weather_data is None:
            error_message = f"Cannot find weather data for {city}. Please try again."
            return render_template('index.html', title=error_message, color=gray)
        current_temp = weather_data["current"]["temp_c"]
        condition = weather_data["current"]["condition"]["text"]
        wind = weather_data["current"]["wind_kph"]
        icon = weather_data["current"]["condition"]["icon"]
        if "sunny" in condition.lower() and current_temp >= 10:
            sunny = '#FD9635'
            title = "Use sunscreen, dummy!"
            return render_template('index.html', city=city, condition=condition, temperature=current_temp, color=sunny, title=title, icon=icon, wind=wind)
        elif "cloudy" in condition.lower() or "overcast" in condition.lower():
            cloudy = "#BFB49D"
            title = "The shade feels nice."
            return render_template('index.html', city=city, condition=condition, temperature=current_temp, color=cloudy, title=title, icon=icon, wind=wind)
        elif "rain" in condition.lower():
            rain = "#2c3c4d"
            title = "Grab an umbrella!"
            return render_template('index.html', city=city, condition=condition, temperature=current_temp, color=rain, title=title, icon=icon, wind=wind)
        elif current_temp <= 5:
            title = "Put on a jacket!"
            return render_template('index.html', city=city, condition=condition, temperature=current_temp, color=rain, title=title, icon=icon, wind=wind)
        elif current_temp <= -5:
            cold = "#4d638f"
            title = "It's really cold out there."
            return render_template('index.html', city=city, condition=condition, temperature=current_temp, color=cold, title=title, icon=icon, wind=wind)
        elif "mist" in condition.lower():
            title = "It might be hard to see."
            return render_template('index.html', city=city, condition=condition, temperature=current_temp, color=gray, title=title, icon=icon, wind=wind)
        else:
            title = "I'm unsure"
            return render_template('index.html', city=city, condition=condition, temperature=current_temp, color=gray, title=title, icon=icon, wind=wind)

    return render_template('index.html', color="#71b5f5", title="How is the weather today?")

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
