# Airflow US Holidays ETL

This project is an ETL (Extract, Transform, Load) pipeline built with Apache Airflow. It extracts public holiday data for the United States from an external API, filters holidays specific to New York, and loads the results into a MySQL database.

## Features

- *Extract:* Fetches US public holidays from 2015 to 2026 using the Nager.Date API.
- *Transform:* Filters holidays to include only those relevant to New York (US-NY).
- *Load:* Inserts the filtered holidays into a MySQL table (us_holidays_airflow).

## Technologies Used

- Apache Airflow
- Python
- MySQL
- Requests, Pendulum

## DAG Overview

- *DAG ID:* etl_us_holidays_airflow
- *Schedule:* Daily
- *Tasks:*
	1. extract_holidays: Extracts all US holidays.
	2. filter_ny_holidays: Filters for New York holidays.
	3. load_to_mysql: Loads data into MySQL.

## Requirements

Install dependencies with:
bash
pip install -r requirements.txt


## Usage

1. Configure your MySQL connection in Airflow (mysql_default).
2. Place the DAG file in your Airflow dags/ directory.
3. Start the Airflow scheduler and webserver.
4. Trigger the DAG from the Airflow UI.

## Table Schema

The MySQL table should have the following columns:
- date, local_name, country_code, fixed, global, counties, launch_year, type, day_of_week

## License

MIT
# Airflow_Holidays-ETL