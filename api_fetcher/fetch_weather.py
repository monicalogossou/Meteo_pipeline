# api_fetcher/fetch_weather.py
import requests
import json
from datetime import datetime
import os

def fetch_and_save(city):
    API_KEY = os.getenv("WEATHER_API_KEY")
    if not API_KEY:
        raise Exception("❌ La variable d'environnement WEATHER_API_KEY est manquante.")
    
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        date_str = datetime.now().strftime("%Y-%m-%d")
        output_dir = f"/data/raw/{city}"
        output_path = f"{output_dir}/{date_str}_weather.json"

        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"[✔] Weather data for {city} saved to {output_path}")
    else:
        print(f"[✘] Failed to fetch weather data for {city}: {response.status_code}")

def fetch_all_cities():
    cities = [
        "Dakar", "Abidjan", "Ouagadougou", "Lome", "Cotonou",
        "Bamako", "Niamey", "Conakry", "Freetown", "Monrovia",
        "Banjul", "Accra"
    ]

    for city in cities:
        fetch_and_save(city)
