#!/usr/bin/env python
# coding: utf-8
"""
ETL Process for Weather Data: Extended Version

This script extracts current weather data for a list of cities using the WeatherAPI,
transforms the data to include additional metadata (such as a generated ID),
and loads the results into both a CSV file and a SQLite database.

Dependencies:
    - os, sqlite3, requests, datetime, pandas

Make sure that you have the required packages installed in your environment.
"""

import os  # Imports the os module to interact with the operating system
import sqlite3  # Imports the sqlite3 module to interact with SQLite databases
import requests  # Imports the requests module to make HTTP requests
import datetime  # Imports the datetime module to handle dates and times
import pandas as pd  # Imports the pandas module to handle dataframes
import mysql.connector


# =============================================================================
# Data Extraction Functions
# =============================================================================

def extract_data_from_api(city):
    """
    Extracts current weather data from WeatherAPI for the given city.

    Args:
        city (str): The city for which to extract weather data.

    Returns:
        pd.DataFrame: A dataframe containing the weather data including temperature,
                      wind speed, `condition`, precipitation, humidity, feels-like temperature,
                      pressure, visibility, day/night indicator, timestamp, and city name.
    """
    # Gets the current date and time for record keeping
    today = datetime.datetime.now()

    # API key - Replace with your actual key after signing up for the WeatherAPI
    key_api_weather = '29407548ea2543e7ac994621251004'

    # Constructs the API endpoint using the provided city
    url = f"http://api.weatherapi.com/v1/current.json?key={key_api_weather}&q={city}&aqi=yes"

    try:
        # Makes a GET request to the WeatherAPI
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data_json = response.json()
    except requests.RequestException as error:
        print(f"Error fetching data for {city}: {error}")
        return pd.DataFrame()  # Return an empty DataFrame in case of failure

    # Extracts and organizes the relevant data fields into a dictionary
    dictionary_data = {
        "city": [city],
        "temperature": [data_json["current"]["temp_c"]],
        "wind_speed": [data_json["current"]["wind_kph"]],
        "condition": [data_json["current"]["condition"]["text"]],
        "precipitation": [data_json["current"]["precip_mm"]],
        "humidity": [data_json["current"]["humidity"]],
        "feels_like_temp": [data_json["current"]["feelslike_c"]],
        "pressure": [data_json["current"]["pressure_mb"]],
        "visibility": [data_json["current"]["vis_km"]],
        "is_day": [data_json["current"]["is_day"]],
        "timestamp": [today]
    }

    # Converts the dictionary to a pandas DataFrame for further processing
    df = pd.DataFrame(dictionary_data)
    return df

# =============================================================================
# Data Quality and Transformation Functions
# =============================================================================

def data_quality_process(df_data):
    """
    Checks the quality of the extracted data by confirming that it is not empty
    and does not contain any missing values.

    Args:
        df_data (pd.DataFrame): The dataframe containing the extracted data.

    Returns:
        bool: Returns False if the data is empty or has missing values, otherwise None.
    """
    if df_data.empty:
        print("Data was not extracted. Please check your API call or city name.")
        return False

    if df_data.isnull().values.any():
        print("Missing values detected. Data cleaning may be necessary.")
        # Optionally, add data cleaning code here

def data_transform_process(df_data):
    """
    Transforms the extracted data for further processing:
        - Converts numeric flags to boolean.
        - Adds a unique "ID" field combining the timestamp, city, and temperature.

    Args:
        df_data (pd.DataFrame): The dataframe containing the extracted data.

    Returns:
        pd.DataFrame: The transformed dataframe ready for loading.
    """
    # Convert the "is_day" column to a boolean (True if day, False if night)
    df_data["is_day"] = df_data["is_day"].astype(bool)
    
    # Create a unique "ID" column combining timestamp, city, and temperature
    df_data["ID"] = (df_data['timestamp'].astype(str) + "-" +
                     df_data["city"] + "-" +
                     df_data["temperature"].astype(str))
    
    return df_data

def extract_transform_process(city):
    """
    Runs the extraction and transformation processes for a given city.

    Args:
        city (str): The name of the city for data extraction.

    Returns:
        pd.DataFrame: The processed dataframe with the extracted data or an empty dataframe if extraction fails.
    """
    # Extract data from the API
    df_data = extract_data_from_api(city)
    # If extraction fails (empty df), skip transformation
    if df_data.empty:
        return df_data
    
    # Transform the extracted data
    df_data = data_transform_process(df_data)
    
    # Check the quality of the data
    data_quality_process(df_data)
    
    return df_data

# =============================================================================
# ETL Main Process
# =============================================================================

def etl_weather():
    """
    Main ETL (Extract, Transform, Load) function for processing weather data.

    Iterates over a predefined list of cities, extracts and transforms weather data for each,
    and then loads the data into a CSV file and a SQLite database.
    """
    # List of cities to extract weather data for.
    cities = [
        "Rio de Janeiro",
        "Sao Paulo",
        "Curitiba",
        "Belo Horizonte",
        "Porto Alegre",
        "Salvador"
    ]

    # Initialize an empty DataFrame to collect all cities' data
    all_data = pd.DataFrame()

    # Iterate over the list of cities
    for city in cities:
        print(f"Processing weather data for {city}...")
        df_city = extract_transform_process(city)
        if df_city.empty:
            print(f"Skipping {city} due to extraction errors.")
            continue
        # Append the city's data to the overall DataFrame
        all_data = pd.concat([all_data, df_city], ignore_index=True)
        load_to_mysql(all_data)


    # =============================================================================
    # Load Process: Saving Data to CSV
    # =============================================================================

    # Define the file path for the CSV file to store the weather data
    file_path = "/opt/airflow/dags/data_weather.csv"

    # Determine whether to include the header by checking if the file exists already
    include_header = not os.path.isfile(file_path)

    try:
        # Save the aggregated data into the CSV file (append mode)
        all_data.to_csv(file_path, mode='a', index=False, header=include_header)
        print(f"Data successfully saved to CSV at {file_path}")
    except Exception as e:
        print(f"Failed to write data to CSV: {e}")

    # =============================================================================
    # Load Process: Saving Data to SQLite Database
    # =============================================================================

    # Define the SQLite database file path
    db_path = "/opt/airflow/dags/database_weather.db"

def load_to_mysql(df):
    try:
        conn = mysql.connector.connect(
            host="mysql",          # Use the service name from docker-compose
            user="weather_user",
            password="weather_pass",
            database="weather_db",
            port=3306
        )
        cursor = conn.cursor()

        # Create table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS data_weather (
            city VARCHAR(50),
            temperature FLOAT,
            wind_speed FLOAT,
            `condition` VARCHAR(100),
            precipitation FLOAT,
            humidity INT,
            feels_like_temp FLOAT,
            pressure FLOAT,
            visibility FLOAT,
            is_day BOOLEAN,
            timestamp DATETIME,
            ID VARCHAR(255) PRIMARY KEY
        )
        """
        cursor.execute(create_table_query)
        conn.commit()

        # Insert each row
        for _, row in df.iterrows():
            insert_query = """
            INSERT IGNORE INTO data_weather (
                city, temperature, wind_speed, `condition`,
                precipitation, humidity, feels_like_temp,
                pressure, visibility, is_day, timestamp, ID
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, tuple(row))
        conn.commit()
        print("Data successfully written to MySQL.")
    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# =============================================================================
# Main Execution Block
# =============================================================================

if __name__ == '__main__':
    print("Starting ETL process for weather data...")
    etl_weather()
    print("ETL process completed.")
    
# =============================================================================
# Additional Comments:
# - This implementation iterates over multiple cities and aggregates the data.
# - Error handling is included to ensure that issues with one city do not halt the process.
# - You may add further logging or data cleaning steps as needed.
# =============================================================================
# This code is designed to be run as a standalone script.
# In a production environment, consider using a task scheduler or orchestration tool
# (like Apache Airflow) to automate the ETL process.
# - Ensure that the database and CSV file paths are accessible and writable.
# - The database connection settings should be adjusted based on your environment.
# - The API key should be kept secure and not hardcoded in production code.
# - Consider using environment variables or a configuration file for sensitive information.