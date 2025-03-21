

# import requests
# import json
# from datetime import datetime, timedelta

# # Define NASA POWER API endpoint
# base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"

# # Define parameters for Raigad district
# params = {
#     "parameters": "T2M,RH2M",  # Temperature, Humidity
#     "community": "RE",  # Renewable Energy Community
#     "longitude": 73.2745,  # Raigad Longitude
#     "latitude": 18.5074,  # Raigad Latitude
#     "start": datetime.today().strftime("%Y%m%d"),  # Start from today
#     "end": (datetime.today() + timedelta(days=30)).strftime("%Y%m%d"),  # 1-month range
#     "format": "JSON",  # Output format
# }

# # Make API request
# response = requests.get(base_url, params=params)

# # Check response status
# if response.status_code == 200:
#     data = response.json()
    
#     # Extract climate data
#     temp_data = data["properties"]["parameter"]["T2M"]
#     humidity_data = data["properties"]["parameter"]["RH2M"]

#     # Pick a forecasted date within the next month
#     forecast_date = None
#     for day in range(30):
#         date = (datetime.today() + timedelta(days=day)).strftime("%Y%m%d")
#         if date in temp_data and temp_data[date] != -999.0:
#             forecast_date = date
#             break  # Stop at the first valid date

#     # Print forecast results
#     print("\n🌍 1-Month Climate Forecast for Raigad District:")
#     if forecast_date:
#         temp = temp_data[forecast_date]
#         humidity = humidity_data[forecast_date]
#         print(f"{forecast_date}: Temp = {temp}°C, Humidity = {humidity}%")
#     else:
#         print("⚠️ No valid data available for the next month.")

# else:
#     print("Error fetching data:", response.status_code)


# import requests
# import xarray as xr
# import numpy as np

# # Define NOAA NOMADS API URL
# NOAA_BASE_URL = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs"
# YEAR = "2025"
# MONTH = "03"  # Forecast for March 2025
# FORECAST_RUN = "06"  # UTC run time

# # Construct the URL for 2m temperature and humidity (CFSv2)
# temp_url = f"{NOAA_BASE_URL}/{YEAR}{MONTH}{FORECAST_RUN}/6hrly_grib_01/tmp2m.grb2"
# humidity_url = f"{NOAA_BASE_URL}/{YEAR}{MONTH}{FORECAST_RUN}/6hrly_grib_01/rhum2m.grb2"

# # Function to download & process NOAA GRIB2 files
# def fetch_noaa_data(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open("forecast_data.grb2", "wb") as f:
#             f.write(response.content)
#         print(f"✅ Data downloaded: {url}")
#         return "forecast_data.grb2"
#     else:
#         print(f"❌ Error fetching data: {url}")
#         return None

# # Fetch temperature & humidity data
# temp_file = fetch_noaa_data(temp_url)
# humidity_file = fetch_noaa_data(humidity_url)

# # Process GRIB2 files using xarray
# if temp_file and humidity_file:
#     temp_data = xr.open_dataset(temp_file, engine="cfgrib")
#     humidity_data = xr.open_dataset(humidity_file, engine="cfgrib")

#     # Extract values for Mumbai (20°N, 72°E approx)
#     temp_mumbai = temp_data["t2m"].sel(latitude=20, longitude=72, method="nearest") - 273.15
#     humidity_mumbai = humidity_data["rhum"].sel(latitude=20, longitude=72, method="nearest")

#     print(f"\n🌍 Climate Forecast for Mumbai (4 Months Ahead):")
#     print(f"🌡️ Avg Temperature: {temp_mumbai.mean().values:.2f}°C")
#     print(f"💧 Avg Humidity: {humidity_mumbai.mean().values:.2f}%")


# import cdsapi

# # Initialize Copernicus API client
# c = cdsapi.Client()

# # Request monthly climate forecast for next 4 months
# c.retrieve(
#     "reanalysis-era5-single-levels-monthly-means",
#     {
#         "format": "netcdf",
#         "variable": ["2m_temperature", "total_precipitation"],
#         "product_type": "monthly_averaged_reanalysis",
#         "year": ["2025"],
#         "month": ["04", "05", "06", "07"],  # Next 4 months
#         "area": [19.0760, 72.8777, 19.0760, 72.8777],  # Mumbai coordinates
#     },
#     "climate_forecast.nc",
# )

# print("✅ Climate forecast data downloaded as 'climate_forecast.nc'")

#### WWWWOOOOORRRRKKKKIIIINNNNGGGG ####
# import requests

# # Set location (latitude, longitude) for Mumbai, India
# latitude = 19.0760
# longitude = 72.8777

# # Correct API Endpoint for Monthly Climate Forecast
# api_url = f"https://climate-api.open-meteo.com/v1/climate?latitude={latitude}&longitude={longitude}&monthly=temperature_2m_mean,relative_humidity_2m_mean&forecast_months=4&timezone=Asia/Kolkata"

# # Make API Request
# response = requests.get(api_url)

# # Check if request was successful
# if response.status_code == 200:
#     data = response.json()
#     print("✅ Monthly Climate Forecast Retrieved Successfully!")
#     print(data)  # Print full JSON response
# else:
#     print(f"❌ Error: {response.status_code} - {response.text}")



import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# 🌍 Define Location (Modify as needed)
latitude = 18.5   # Example: Raigad
longitude = 73.2
start_year = 1980
end_year = 2024

# 📡 Fetch historical climate data
print("📡 Fetching historical climate data from Open-Meteo...")

url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_year}-01-01&end_date={end_year}-12-31&daily=temperature_2m_max,relative_humidity_2m_max&timezone=auto"

response = requests.get(url)
if response.status_code != 200:
    print(f"❌ Error: {response.status_code} - {response.json()}")
    exit()

data = response.json()

# 🗂 Convert Data to Pandas DataFrame
dates = pd.to_datetime(data["daily"]["time"])
df = pd.DataFrame({
    "date": dates,
    "year": pd.Series(dates).dt.year,
    "month": pd.Series(dates).dt.month,
    "temperature_2m_max": data["daily"]["temperature_2m_max"],
    "relative_humidity_2m_max": data["daily"]["relative_humidity_2m_max"]
})

# 📈 Aggregate Monthly Data
df_monthly = df.groupby(["year", "month"]).mean().reset_index()

# 🚀 Predict Future Trends Using Linear Regression
def predict_future_trends(variable, months_ahead=4):
    X = df_monthly[["year", "month"]].values
    y = df_monthly[variable].values

    # Train Linear Regression Model
    model = LinearRegression()
    model.fit(X, y)

    # Generate future months
    last_year, last_month = df_monthly[["year", "month"]].iloc[-1]
    future_dates = []
    for _ in range(months_ahead):
        last_month += 1
        if last_month > 12:
            last_year += 1
            last_month = 1
        future_dates.append([last_year, last_month])

    future_dates = np.array(future_dates)
    predictions = model.predict(future_dates)

    return future_dates, predictions

# 🎯 Predict Next 4 Months
future_temp_dates, future_temp = predict_future_trends("temperature_2m_max")
future_hum_dates, future_hum = predict_future_trends("relative_humidity_2m_max")

# 📊 Display Predictions
print("\n📌 **4-Month Temperature Prediction**")
for i in range(4):
    print(f"{future_temp_dates[i][0]}-{future_temp_dates[i][1]:02d}: {future_temp[i]:.2f}°C")

print("\n📌 **4-Month Humidity Prediction**")
for i in range(4):
    print(f"{future_hum_dates[i][0]}-{future_hum_dates[i][1]:02d}: {future_hum[i]:.2f}% RH")

# 📉 Plot Results
plt.figure(figsize=(12, 6))

# Temperature Plot
plt.subplot(2, 1, 1)
plt.plot(df_monthly.index, df_monthly["temperature_2m_max"], label="Historical Temperature", color='blue')
plt.plot(range(len(df_monthly), len(df_monthly) + 4), future_temp, 'ro--', label="Predicted Temperature")
plt.title("Temperature Trend & Prediction")
plt.xlabel("Months")
plt.ylabel("Temperature (°C)")
plt.legend()

# Humidity Plot
plt.subplot(2, 1, 2)
plt.plot(df_monthly.index, df_monthly["relative_humidity_2m_max"], label="Historical Humidity", color='green')
plt.plot(range(len(df_monthly), len(df_monthly) + 4), future_hum, 'ro--', label="Predicted Humidity")
plt.title("Humidity Trend & Prediction")
plt.xlabel("Months")
plt.ylabel("Humidity (% RH)")
plt.legend()

# Show the combined plots
plt.tight_layout()
plt.show()
