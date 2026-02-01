# Weather & Stock Price Fetcher

A simple Python script to fetch current weather data for New York City and the latest Microsoft (MSFT) stock price.

## Features

- 🌤️ **Weather Data**: Current temperature, conditions, humidity, and wind speed for NYC
- 📈 **Stock Price**: Latest MSFT price with daily change and percentage
- 🔑 **No API Keys Required**: Uses free, open APIs
- 🐍 **Pure Python**: Only requires `requests` library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AsTheSeaRises/weather-stock-fetcher.git
cd weather-stock-fetcher
```

2. Install dependencies:
```bash
pip install requests
```

## Usage

Run the script:

```bash
python3 weather_stock_fetcher.py
```

### Example Output

```
==================================================
Weather & Stock Report - 2026-02-01 20:55:00
==================================================

🌤️  New York Weather
------------------------------
Temperature: 42.5°F
Condition: Partly cloudy
Humidity: 65%
Wind Speed: 8 mph

📈 Microsoft (MSFT) Stock
------------------------------
Price: $412.35 USD
Change: 📈 $3.45 (+0.84%)
Exchange: NasdaqGS

==================================================
```

## APIs Used

- **Weather**: [Open-Meteo](https://open-meteo.com/) — Free weather API with no authentication required
- **Stock Price**: [Yahoo Finance](https://finance.yahoo.com/quote/MSFT) — Unofficial endpoint for market data

## Customisation

Want to track a different city or stock? Edit these variables in the script:

```python
# Change coordinates for different location
lat, lon = 40.7128, -74.0060  # New York City

# Change stock symbol
symbol = "MSFT"  # Try "AAPL", "GOOGL", "TSLA", etc.
```

## License

MIT License — feel free to use and modify as you like.
