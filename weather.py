#!/usr/bin/env python3
"""
Weather Information Display Program
Fetches and displays current weather data using Open-Meteo API (no API key required)
"""

import requests
import sys
from datetime import datetime


def get_coordinates(city_name):
    """Get latitude and longitude for a city name using Geocoding API."""
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    
    try:
        response = requests.get(geocoding_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return {
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "name": result["name"],
                "country": result.get("country", "")
            }
        else:
            return None
    except requests.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return None


def get_weather_data(latitude, longitude):
    """Fetch current weather data from Open-Meteo API."""
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "weather_code",
            "wind_speed_10m",
            "wind_direction_10m",
            "precipitation",
            "cloud_cover"
        ],
        "timezone": "auto"
    }
    
    try:
        response = requests.get(weather_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def get_weather_description(weather_code):
    """Convert WMO weather code to human-readable description."""
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_codes.get(weather_code, "Unknown")


def display_weather(city_info, weather_data):
    """Display formatted weather information."""
    current = weather_data.get("current", {})
    
    print("\n" + "=" * 50)
    print(f"🌍 Weather Information for {city_info['name']}, {city_info['country']}")
    print("=" * 50)
    print(f"📅 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    print(f"🌡️  Temperature:        {current.get('temperature_2m', 'N/A')}°C")
    print(f"🤔 Feels like:          {current.get('apparent_temperature', 'N/A')}°C")
    print(f"☁️  Condition:           {get_weather_description(current.get('weather_code', -1))}")
    print(f"💧 Humidity:            {current.get('relative_humidity_2m', 'N/A')}%")
    print(f"💨 Wind Speed:          {current.get('wind_speed_10m', 'N/A')} km/h")
    print(f"🧭 Wind Direction:      {current.get('wind_direction_10m', 'N/A')}°")
    print(f"🌧️  Precipitation:       {current.get('precipitation', 'N/A')} mm")
    print(f"☁️  Cloud Cover:         {current.get('cloud_cover', 'N/A')}%")
    print("=" * 50 + "\n")


def main():
    """Main function to run the weather program."""
    # Default city or get from command line
    if len(sys.argv) > 1:
        city_name = " ".join(sys.argv[1:])
    else:
        city_name = input("Enter city name: ").strip()
    
    if not city_name:
        print("No city name provided. Exiting.")
        sys.exit(1)
    
    print(f"\n🔍 Searching for weather in '{city_name}'...")
    
    # Get city coordinates
    city_info = get_coordinates(city_name)
    if not city_info:
        print(f"❌ Could not find city: {city_name}")
        sys.exit(1)
    
    # Get weather data
    weather_data = get_weather_data(city_info["latitude"], city_info["longitude"])
    if not weather_data:
        print("❌ Could not fetch weather data.")
        sys.exit(1)
    
    # Display weather information
    display_weather(city_info, weather_data)


if __name__ == "__main__":
    main()
