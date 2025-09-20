# Airbyte Weather ETL

This project uses Airbyte to extract weather data from the Open-Meteo API and load it into a MySQL database.

## Overview
- **Source:** Open-Meteo API (https://open-meteo.com/)
- **Destination:** MySQL Database
- **ETL Tool:** Airbyte

## How It Works
1. **Extract:** Airbyte connects to the Open-Meteo API to fetch weather data (such as temperature, humidity, wind speed, etc.).
2. **Load:** The extracted data is loaded directly into a MySQL database using Airbyte's MySQL connector.
3. **Transform (Optional):** You can add transformations using Airbyte's normalization or dbt integration if needed.

## Setup Instructions
1. **Install Airbyte:**
   - Follow the official Airbyte documentation to install and run Airbyte locally or on a server.
2. **Configure Source Connector:**
   - Add a new source in Airbyte and select "HTTP API" or a custom connector for Open-Meteo.
   - Set the API endpoint and parameters as needed.
3. **Configure Destination Connector:**
   - Add a new destination in Airbyte and select "MySQL".
   - Provide your MySQL connection details (host, port, database, username, password).
4. **Create and Run Connection:**
   - Set up a connection between the source and destination.
   - Schedule syncs as required (manual or automatic).

## Example Use Case
- Automate daily weather data collection for analytics or reporting.
- Store historical weather data for machine learning or forecasting.

## References
- [Airbyte Documentation](https://docs.airbyte.com/)
- [Open-Meteo API Docs](https://open-meteo.com/en/docs)
