# Weather Data Collection Project

## Project Overview
This Python project collects historical and forecasted weather data (actual & forecast) for New York City using the Open-Meteo API. The results are saved in a CSV file, a SQLite database, and a MySQL database.

## Features
- Fetches weather data (temperature, precipitation, wind speed, snowfall) from 2015 until today, plus a 12-day forecast.
- Merges actual and forecast data into a single file.
- Saves data to:
	- CSV file
	- SQLite database
	- MySQL database

## Requirements
- Python 3.7 or higher
- Libraries:
	- requests
	- pandas
	- mysql-connector-python
	- sqlite3 (included with Python)

To install requirements:
bash
pip install requests pandas mysql-connector-python


## Usage
1. Make sure you have a MySQL database named weather_project and a table named weather_data with the appropriate fields.
2. Edit the database connection details in the script if needed (host, user, password).
3. Run the script:
bash
python weather_project_HOH\ (3).py

4. You will find the results in:
	 - weather_data.csv file
	 - SQLite database weather_data.db
	 - MySQL database table weather_data

## Notes
- The script merges actual and forecast data and updates MySQL automatically.
- You must have write access to the databases.
- You can change the coordinates (latitude, longitude) for any other city.

## Example MySQL Table:
sql
CREATE TABLE weather_data (
		time DATE PRIMARY KEY,
		temperature_2m_max FLOAT,
		temperature_2m_min FLOAT,
		precipitation_sum FLOAT,
		windspeed_10m_max FLOAT,
		snowfall_sum FLOAT,
		type CHAR(1)
);


---
Project by Tsbeeh Mohamed
