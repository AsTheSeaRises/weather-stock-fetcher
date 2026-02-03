#!/usr/bin/env python3
"""
London Weather Fetcher
Retrieves current weather and forecast for London using wttr.in API.
No API key required.
"""

import requests
from datetime import datetime


def get_london_weather():
    """
    Fetch current weather for London from wttr.in.
    
    Returns:
        dict: Weather data including temperature, condition, humidity, and wind
    """
    # Using wttr.in format codes:
    # %l = location, %c = condition (emoji), %t = temperature,
    # %h = humidity, %w = wind
    url = "https://wttr.in/London?format=%l:+%c+%t+%h+%w"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse the response
        weather_data = response.text.strip()
        
        return {
            "raw": weather_data,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "success": True
        }
    
    except requests.RequestException as e:
        return {
            "error": str(e),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "success": False
        }


def get_detailed_forecast():
    """
    Fetch detailed forecast for London.
    
    Returns:
        str: Multi-line weather forecast
    """
    url = "https://wttr.in/London?T"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    
    except requests.RequestException as e:
        return f"Error fetching forecast: {e}"


def main():
    """Main function to display London weather."""
    print("=" * 50)
    print("London Weather - {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    print("=" * 50)
    
    # Get current weather
    weather = get_london_weather()
    
    if weather["success"]:
        print("\n📍 Current Weather:")
        print(weather["raw"])
    else:
        print(f"\n❌ Error: {weather['error']}")
    
    print("\n" + "=" * 50)
    print("Full Forecast:")
    print("=" * 50)
    
    # Get detailed forecast
    forecast = get_detailed_forecast()
    print(forecast)


if __name__ == "__main__":
    main()
