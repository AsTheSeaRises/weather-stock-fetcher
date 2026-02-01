#!/usr/bin/env python3
"""
Weather and Stock Price Fetcher
Gets current weather for New York and latest Microsoft (MSFT) stock price.
"""

import requests
import os
from datetime import datetime


def get_weather_ny():
    """Fetch current weather for New York using Open-Meteo API (no key required)."""
    # New York City coordinates
    lat, lon = 40.7128, -74.0060
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "weather_code", "wind_speed_10m"],
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "timezone": "America/New_York"
    }
    
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    
    current = data["current"]
    weather_code = current["weather_code"]
    
    # Weather code mapping (simplified)
    weather_descriptions = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        95: "Thunderstorm"
    }
    
    weather_desc = weather_descriptions.get(weather_code, "Unknown")
    
    return {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "condition": weather_desc
    }


def get_msft_stock():
    """Fetch latest Microsoft stock price using Yahoo Finance API (unofficial)."""
    # Using Yahoo Finance quote endpoint
    symbol = "MSFT"
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    
    params = {
        "interval": "1d",
        "range": "1d"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0"
    }
    
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    
    result = data["chart"]["result"][0]
    meta = result["meta"]
    
    # Get the latest price
    timestamps = result.get("timestamp", [])
    closes = result["indicators"]["quote"][0].get("close", [])
    
    if closes:
        latest_price = closes[-1]
    else:
        latest_price = meta.get("regularMarketPrice", "N/A")
    
    previous_close = meta.get("previousClose", "N/A")
    
    # Calculate change
    if isinstance(latest_price, (int, float)) and isinstance(previous_close, (int, float)):
        change = latest_price - previous_close
        change_percent = (change / previous_close) * 100
    else:
        change = "N/A"
        change_percent = "N/A"
    
    return {
        "symbol": symbol,
        "price": latest_price,
        "change": change,
        "change_percent": change_percent,
        "currency": meta.get("currency", "USD"),
        "exchange": meta.get("exchangeName", "Unknown")
    }


def main():
    """Main function to fetch and display weather and stock data."""
    print("=" * 50)
    print(f"Weather & Stock Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Get weather
    print("\n🌤️  New York Weather")
    print("-" * 30)
    try:
        weather = get_weather_ny()
        print(f"Temperature: {weather['temperature']:.1f}°F")
        print(f"Condition: {weather['condition']}")
        print(f"Humidity: {weather['humidity']}%")
        print(f"Wind Speed: {weather['wind_speed']} mph")
    except Exception as e:
        print(f"Error fetching weather: {e}")
    
    # Get stock price
    print("\n📈 Microsoft (MSFT) Stock")
    print("-" * 30)
    try:
        stock = get_msft_stock()
        print(f"Price: ${stock['price']:.2f} {stock['currency']}")
        if isinstance(stock['change'], (int, float)):
            change_symbol = "📈" if stock['change'] >= 0 else "📉"
            print(f"Change: {change_symbol} ${stock['change']:.2f} ({stock['change_percent']:+.2f}%)")
        else:
            print(f"Change: N/A")
        print(f"Exchange: {stock['exchange']}")
    except Exception as e:
        print(f"Error fetching stock price: {e}")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
