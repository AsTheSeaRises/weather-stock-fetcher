#!/usr/bin/env python3
"""
London Weather Checker
Fetches current weather data for London using Open-Meteo API (no API key required)
"""

import requests
import json
from datetime import datetime


def get_london_weather():
    """Fetch current weather for London."""
    # London coordinates
    lat = 51.5074
    lon = -0.1278
    
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
        f"precipitation,weather_code,wind_speed_10m,wind_direction_10m"
        f"&timezone=Europe/London"
    )
    
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_weather_description(code):
    """Convert WMO weather code to description."""
    codes = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        56: "Light freezing drizzle", 57: "Dense freezing drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        66: "Light freezing rain", 67: "Heavy freezing rain",
        71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        85: "Slight snow showers", 86: "Heavy snow showers",
        95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
    }
    return codes.get(code, "Unknown")


def format_weather(data):
    """Format weather data into a readable string."""
    current = data.get("current", {})
    
    temp = current.get("temperature_2m", "N/A")
    feels_like = current.get("apparent_temperature", "N/A")
    humidity = current.get("relative_humidity_2m", "N/A")
    wind_speed = current.get("wind_speed_10m", "N/A")
    precipitation = current.get("precipitation", "N/A")
    weather_code = current.get("weather_code", 0)
    
    description = get_weather_description(weather_code)
    
    output = f"""
╔════════════════════════════════════════╗
║     London Weather - {datetime.now().strftime("%H:%M")}          ║
╠════════════════════════════════════════╣
║  {description:36} ║
║                                        ║
║  🌡️  Temperature:   {temp}°C                     ║
║  🤔  Feels like:    {feels_like}°C                     ║
║  💧  Humidity:      {humidity}%                     ║
║  🌧️  Precipitation: {precipitation}mm                     ║
║  💨  Wind:          {wind_speed} km/h                    ║
╚════════════════════════════════════════╝
"""
    return output.strip()


def main():
    try:
        data = get_london_weather()
        print(format_weather(data))
        
        # Also output as JSON for piping
        print("\n" + "="*40)
        print("JSON Output:")
        print(json.dumps(data, indent=2))
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
