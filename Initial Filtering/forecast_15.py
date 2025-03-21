import requests

# Replace this with your Weatherbit API key
API_KEY = "277c178bf1c843628600849faa126f32"
CITY = "Raigad"

# Get city coordinates using Weatherbit API
geocoding_url = f"https://api.weatherbit.io/v2.0/current?city={CITY}&key={API_KEY}"
response = requests.get(geocoding_url)

if response.status_code == 200:
    data = response.json()
    if 'data' in data and data['data']:
        lat = data['data'][0]['lat']
        lon = data['data'][0]['lon']

        # Fetch 15-day weather forecast
        forecast_url = f"https://api.weatherbit.io/v2.0/forecast/daily?lat={lat}&lon={lon}&days=15&key={API_KEY}&units=M"
        forecast_response = requests.get(forecast_url)

        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()

            print(f"\n📅 15-Day Weather Forecast for {CITY}:")
            print("-" * 40)

            for day in forecast_data['data']:
                date = day['datetime']
                temp = day['temp']
                humidity = day['rh']
                weather_desc = day['weather']['description']

                print(f"📆 Date: {date}")
                print(f"🌡️ Temperature: {temp}°C")
                print(f"💧 Humidity: {humidity}%")
                print(f"🌤️ Condition: {weather_desc}")
                print("-" * 40)

        else:
            print("Error fetching 15-day forecast:", forecast_response.status_code, forecast_response.json())
    else:
        print("City not found in Weatherbit database.")
else:
    print("Error fetching city coordinates:", response.status_code)


# import requests

# # Replace with your city and country code
# CITY = "Raigad"
# LAT = 18.5  # Latitude of Raigad
# LON = 73.2  # Longitude of Raigad

# # Open-Meteo API URL
# forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&daily=temperature_2m_max,relative_humidity_2m_max&timezone=auto"

# # Fetch weather data
# response = requests.get(forecast_url)

# if response.status_code == 200:
#     data = response.json()
#     forecast_dates = data["daily"]["time"]
#     temperatures = data["daily"]["temperature_2m_max"]
#     humidities = data["daily"]["relative_humidity_2m_max"]

#     print("\n📅 16-Day Weather Forecast for Raigad:")
#     print("-" * 40)

#     for i in range(len(forecast_dates)):
#         print(f"📆 Date: {forecast_dates[i]}")
#         print(f"🌡️ Temperature: {temperatures[i]}°C")
#         print(f"💧 Humidity: {humidities[i]}%")
#         print("-" * 40)

# else:
#     print("Error fetching forecast:", response.status_code)
