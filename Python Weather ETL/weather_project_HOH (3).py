import requests
import pandas as pd
from datetime import datetime, timedelta
import sqlite3
import mysql.connector

latitude = 40.7128
longitude = -74.0060

start_date = "2015-01-01"
today = datetime.today()
end_date = today.strftime("%Y-%m-%d")
future_date = (today + timedelta(days=12)).strftime("%Y-%m-%d")

archive_url = "https://archive-api.open-meteo.com/v1/archive"
forecast_url = "https://api.open-meteo.com/v1/forecast"

params_actual = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": start_date,
    "end_date": end_date,
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "windspeed_10m_max",
        "snowfall_sum"
    ],
    "temperature_unit": "fahrenheit",
    "windspeed_unit": "mph",
    "precipitation_unit": "inch",
    "snowfall_unit": "inch",
    "timezone": "auto"
}

params_forecast = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": today.strftime("%Y-%m-%d"),
    "end_date": future_date,
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "windspeed_10m_max",
        "snowfall_sum"
    ],
    "temperature_unit": "fahrenheit",
    "windspeed_unit": "mph",
    "precipitation_unit": "inch",
    "snowfall_unit": "inch",
    "timezone": "auto"
}

response_actual = requests.get(archive_url, params=params_actual, timeout=30)
response_forecast = requests.get(forecast_url, params=params_forecast, timeout=30)

data_actual = response_actual.json()
data_forecast = response_forecast.json()

df_actual = pd.DataFrame(data_actual["daily"])
df_actual["type"] = "A"  # Actual

df_forecast = pd.DataFrame(data_forecast["daily"])
df_forecast["type"] = "P"  # Prediction

df_merged = pd.concat([df_actual, df_forecast], ignore_index=True)
df_merged["time"] = pd.to_datetime(df_merged["time"])
df_merged = df_merged.sort_values("time").reset_index(drop=True)

# CSV
df_merged.to_csv("weather_data.csv", index=False)

# SQLite
conn = sqlite3.connect("weather_data.db")
df_merged.to_sql("weather", conn, if_exists="replace", index=False)
conn.close()

# MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="weather_project"
)

cursor = conn.cursor()

cursor.execute("SELECT time, type FROM weather_data")
existing_rows = cursor.fetchall()
existing_data = {(row[0], row[1]) for row in existing_rows}
df_merged = df_merged.where(pd.notnull(df_merged), None)

rows_to_update = []
for index, row in df_merged.iterrows():
    date_key = (row["time"].date(), row["type"])
    if date_key not in existing_data or row["type"] == "A":
        row_data = [
            row["time"].date(),
            row["temperature_2m_max"],
            row["temperature_2m_min"],
            row["precipitation_sum"],
            row["windspeed_10m_max"],
            row["snowfall_sum"],
            row["type"]
        ]
        cleaned_row = [None if pd.isna(val) else val for val in row_data]
        rows_to_update.append(tuple(cleaned_row))

for row in rows_to_update:
    cursor.execute("""
        REPLACE INTO weather_data (
            time, temperature_2m_max, temperature_2m_min,
            precipitation_sum, windspeed_10m_max, snowfall_sum, type
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, row)

conn.commit()
cursor.close()
conn.close()

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="weather_project"
    )
    print("Connection successful!")
    conn.close()
except mysql.connector.Error as err:
    print("Error:", err)