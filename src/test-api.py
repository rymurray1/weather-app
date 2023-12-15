import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": [39.1646, 38.9353, 38.684, 37.630768, 39.27484, 39.197, 39.30444, 39.6341, 39.182, 39.1863, 39.6042, 39.4783, 39.479, 38.901, 39.5817, 39.6801, 37.63027, 39.213, 40.485, 37.9167, 39.6061, 39.88332, 37.474759, 48.376, 43.6971, 45.0314, 44.4734, 45.2778, 45.8174, 48.407, 36.596, 44.3659, 43.979282, 45.331845, 40.5777, 40.6, 40.6226, 40.6505, 41.379, 41.2006, 40.5829, 40.615139, 43.6094, 42.9602, 44.5275, 44.135098, 46.9282, 47.4246, 43.818, 43.5942],
	"longitude": [-120.2387, -119.94, -120.068, -119.032631, -120.1206, -120.2357, -120.33583, -105.8715, -106.8564, -106.8182, -106.5165, -106.0723, -106.1613, -106.9672, -105.9437, -105.898, -107.814045, -106.9378, -106.8317, -107.8375, -106.355, -105.773896, -106.793583, -116.6171, -114.3517, -70.3131, -70.8569, -111.4103, -110.8966, -114.3373, -105.4545, -73.9026, -121.688366, -121.664981, -111.624, -111.58333, -111.4851, -111.5045, -111.7807, -111.8614, -111.6556, -111.588917, -72.7968, -72.9204, -72.7839, -72.885962, -121.5045, -121.4164, -110.701, -110.8437],
	# "hourly": ["temperature_2m", "snowfall"],
	"daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_gusts_10m_max"],
	"temperature_unit": "fahrenheit",
	"wind_speed_unit": "mph",
	"precipitation_unit": "inch"
}

responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
#response = responses[0]
for response in responses:
	print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
	print(f"Elevation {response.Elevation()} m asl")
	print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
	print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

	# Process hourly data. The order of variables needs to be the same as requested.
	# hourly = response.Hourly()
	# hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	# hourly_snowfall = hourly.Variables(1).ValuesAsNumpy()

	# hourly_data = {"date": pd.date_range(
	# 	start = pd.to_datetime(hourly.Time(), unit = "s"),
	# 	end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
	# 	freq = pd.Timedelta(seconds = hourly.Interval()),
	# 	inclusive = "left"
	# )}
	# hourly_data["temperature_2m"] = hourly_temperature_2m
	# hourly_data["snowfall"] = hourly_snowfall

	# hourly_dataframe = pd.DataFrame(data = hourly_data)
	# print(hourly_dataframe)

	# Process daily data. The order of variables needs to be the same as requested.
	daily = response.Daily()
	daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
	daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
	daily_precipitation_sum = daily.Variables(2).ValuesAsNumpy()
	daily_wind_gusts_10m_max = daily.Variables(3).ValuesAsNumpy()

	daily_data = {"date": pd.date_range(
		start = pd.to_datetime(daily.Time(), unit = "s"),
		end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
		freq = pd.Timedelta(seconds = daily.Interval()),
		inclusive = "left"
	)}
	daily_data["temperature_2m_max"] = daily_temperature_2m_max
	daily_data["temperature_2m_min"] = daily_temperature_2m_min
	daily_data["precipitation_sum"] = daily_precipitation_sum
	daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max

	daily_dataframe = pd.DataFrame(data = daily_data)
	print(daily_dataframe)