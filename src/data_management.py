import requests


def get_weather(city):
    api_key = "2ff8e9d24a2cc365df35ebf3795b8af3"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    full_url = f"{base_url}appid={api_key}&q={city}&units=metric"
    response = requests.get(full_url)
    data = response.json()
    if data["cod"] == 200:
        weather_info = {
            'Miestas': city,
            'Temperatūra': data["main"]["temp"],
            'Slėgis': data["main"]["pressure"],
            'Drėgnumas': data["main"]["humidity"],
            'Vėjas': data.get('wind', {}).get('speed', 'N / A'),
            'Aprašymas': data["weather"][0]["description"],

        }
        return weather_info
    else:
        raise ValueError(f"Miestas '{city}' nerastas arba įvyko kita klaida.")


