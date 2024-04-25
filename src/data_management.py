import requests


def get_weather(city):
    api_key = ""
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    full_url = f"{base_url}appid={api_key}&q={city}&units=metric"
    response = requests.get(full_url)
    data = response.json()
    if data["cod"] == 200:
        weather_info = {
            'City': city,
            'Temperature': data["main"]["temp"],
            'Pressure': data["main"]["pressure"],
            'Humidity': data["main"]["humidity"],
            'Wind': data.get('wind', {}).get('speed', 'N / A'),
            'Description': data["weather"][0]["description"],
        }
        return weather_info
    else:
        raise ValueError(f"City '{city}' not found or other error occurred.")
