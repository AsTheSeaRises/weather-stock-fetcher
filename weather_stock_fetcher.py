#!/usr/bin/env python3
"""
London Weather & Microsoft Stock Price Fetcher
Retrieves current weather for London and Microsoft (MSFT) stock price.
No API keys required for basic functionality.
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
        
        return {
            "location": "London",
            "data": response.text.strip(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "success": True
        }
    
    except requests.RequestException as e:
        return {
            "location": "London",
            "error": str(e),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "success": False
        }


def get_microsoft_stock():
    """
    Fetch Microsoft (MSFT) stock price from Yahoo Finance API.
    
    Returns:
        dict: Stock data including current price, change, and market status
    """
    symbol = "MSFT"
    # Using Yahoo Finance's query API (no key required)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant data from the response
        quote = data['chart']['result'][0]
        meta = quote['meta']
        
        current_price = meta['regularMarketPrice']
        previous_close = meta['previousClose']
        change = current_price - previous_close
        change_percent = (change / previous_close) * 100
        
        return {
            "symbol": symbol,
            "company": "Microsoft Corporation",
            "price": current_price,
            "previous_close": previous_close,
            "change": change,
            "change_percent": change_percent,
            "currency": meta['currency'],
            "market_state": meta['marketState'],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "success": True
        }
    
    except (requests.RequestException, KeyError, IndexError) as e:
        return {
            "symbol": symbol,
            "error": str(e),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "success": False
        }


def format_stock_display(stock_data):
    """
    Format stock data for clean display.
    
    Args:
        stock_data (dict): Stock information dictionary
        
    Returns:
        str: Formatted stock information
    """
    if not stock_data["success"]:
        return f"❌ Error fetching stock data: {stock_data['error']}"
    
    # Determine if price went up or down
    change_symbol = "📈" if stock_data["change"] >= 0 else "📉"
    change_sign = "+" if stock_data["change"] >= 0 else ""
    
    output = f"""
📊 {stock_data['company']} ({stock_data['symbol']})
💰 Current Price: ${stock_data['price']:.2f} {stock_data['currency']}
{change_symbol} Change: {change_sign}${stock_data['change']:.2f} ({change_sign}{stock_data['change_percent']:.2f}%)
📍 Previous Close: ${stock_data['previous_close']:.2f}
🕐 Market Status: {stock_data['market_state']}
"""
    return output.strip()


def main():
    """Main function to display London weather and Microsoft stock price."""
    print("=" * 60)
    print(f"London Weather & Microsoft Stock - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Get London weather
    print("\n🌤️  LONDON WEATHER")
    print("-" * 60)
    weather = get_london_weather()
    
    if weather["success"]:
        print(weather["data"])
    else:
        print(f"❌ Error: {weather['error']}")
    
    # Get Microsoft stock price
    print("\n" + "=" * 60)
    print("📈 MICROSOFT STOCK (MSFT)")
    print("-" * 60)
    stock = get_microsoft_stock()
    print(format_stock_display(stock))
    
    print("\n" + "=" * 60)
    print(f"Data retrieved at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


if __name__ == "__main__":
    main()
