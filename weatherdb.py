#!/usr/bin/python3

# Author: O.A.

# A simple app that saves location and weather data into an SQLite database and displays it

import sqlite3
import urllib.request, urllib.parse, urllib.error
import json

import credentials
API_KEY = credentials.OpenWeatherMapCredentials()["APPID"]

# Create or connect to database
dbconnnection = sqlite3.connect('weatherdb.sqlite'); # creates database on disk, in the directory from where this program is invoked
dbcursor = dbconnnection.cursor()

# Available input options for the CMD:
# - A location name, e.g. "Kvevlax, Finland", to search a location and add or update its weather data in the database
# - "#view" to display the database in its entirety
# - "#clear" to clear the whole database
# - "#quit" to quit the program


### FUNCTION DEFINITIONS START

def init_db():
    # Initializes database by destroying it and rebuilding its structure from scratch
    # Side-effects only - does not return anything

    dbcursor.executescript('''
        DROP TABLE IF EXISTS "Places";
        DROP TABLE IF EXISTS "Countries";
        DROP TABLE IF EXISTS "Timezones";
        DROP TABLE IF EXISTS "Weather_conditions";

        CREATE TABLE "Places" (
        "id"	INTEGER NOT NULL UNIQUE,
        "name"	TEXT NOT NULL,
        "lat"	REAL NOT NULL,
        "lon"	REAL NOT NULL,
        "temp"	REAL NOT NULL,
        "country_id"	INTEGER NOT NULL,
        "timezone_id"	INTEGER NOT NULL,
        "weather_conditions_id"	INTEGER NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT),
        FOREIGN KEY("country_id") REFERENCES "Countries"("id"),
        FOREIGN KEY("timezone_id") REFERENCES "Timezones"("id"),
        FOREIGN KEY("weather_conditions_id") REFERENCES "Weather_conditions"("id"),
        UNIQUE("lat","lon") ON CONFLICT REPLACE
        );

        CREATE TABLE "Countries" (
            "id"	INTEGER NOT NULL UNIQUE,
            "name"	TEXT NOT NULL UNIQUE,
            PRIMARY KEY("id" AUTOINCREMENT)
        );

        CREATE TABLE "Timezones" (
            "id"	INTEGER NOT NULL UNIQUE,
            "name"	TEXT NOT NULL UNIQUE,
            PRIMARY KEY("id" AUTOINCREMENT)
        );

        CREATE TABLE "Weather_conditions" (
            "id"	INTEGER NOT NULL UNIQUE,
            "description"	TEXT NOT NULL UNIQUE,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
    ''')

def request_weather_data(location):

    # This function returns a dictionary, i.e.
    #       {
    #       "success" : <boolean>,
    #       "error_description" : <string>,
    #       "geocoding_data" : <dictionary>, i.e. geocoding_data[0], (only if "success" : True)
    #       "weather_data" : <dictionary>, i.e. weather_data, (only if "success" : True)
    #       }

    # URL encode the location's plaintext name (e.g. "Kvevlax, Finland" must become "Kvevlax%2C+Finland").
    location_urlencoded = urllib.parse.urlencode({'' : location})[1:] # en fuling? Turns e.g. "=Kvevlax%2C+Finland" into just "Kvevlax%2C+Finland"

    # Query OpenWeatherMap Geocoding API to get geographical coordinates for the location        
    # Ask only for the very first match and assume that it is the correct location that the user wanted ("&limit=1")
    request_string_geocoding = "http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={appid}".format(location=location_urlencoded, appid=API_KEY)

    try:
        geocoding_response = urllib.request.urlopen(request_string_geocoding).read().decode() # read the whole API response # the returned object works like an "fhand"
    except Exception as err:
        return {
            "success" : False,
            "error_description" : "Error - Could not retrieve geocoding data - " + str(err)
            }

    geocoding_data = json.loads(geocoding_response) # returns a dictionary
    
    if len(geocoding_data) == 0: # error checking, was the searched location found?
        return {
            "success" : False,
            "error_description" : "Error - Could not find location, try again"
            }

    print() # output spacer

    # Query the OpenWeatherMap One Call 3.0 API to get the weather data for the location
    # 
    request_string_weather = "https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily,alerts&units=metric&appid={appid}".format(lat=geocoding_data[0]["lat"], lon=geocoding_data[0]["lon"], appid=API_KEY)

    try:
        weather_response = urllib.request.urlopen(request_string_weather).read().decode() # read the whole API response # the returned object works like an "fhand"
    except Exception as err:
        return {
            "success" : False,
            "error_description" : "Error - Could not retrieve weather data - " + str(err)
            }

    weather_data = json.loads(weather_response) # returns a dictionary
    
    if len(weather_data) == 0: # error checking, is there any weather data? (it's unlikely that it would be missing, but still...)
        return {
            "success" : False,
            "error_description" : "Error - No weather data for the location (this is very unexpected!)"
            }

    return {
        "success" : True,
        "error_description" : "",
        "geocoding_data" : geocoding_data[0],
        "weather_data" : weather_data
    }

### FUNCTION DEFINITIONS END

while True:
    inputline = input("> ")
    
    print() # output spacer

    if not(inputline.startswith("#")): # If line doesn't start with a #, treat user's input as the plaintext name of the location that we must get the weather information for

        open_weater_map_response = request_weather_data(inputline)
        
        if open_weater_map_response["success"] == False: # error handling
            print(open_weater_map_response["error_description"])
            continue

        # TODO grab the relevant location and weather data information and process it appropriately
        print(open_weater_map_response["geocoding_data"]) # debug
        print(open_weater_map_response["weather_data"]) # debug

        # TODO: Add location and weather data to SQLite database in appropriate fashion

    else: # Treat user's input like a command and check against the defined commands for this program
        if inputline == "#view":
            # TODO
            print("Not yet implemented - VIEW DATABASE")

        elif inputline == "#clear":
            # TODO
            print("Not yet implemented - CLEAR DATABASE")
            
        elif inputline == "#quit":
            break

        else:
            print("Invalid command")

# Program finishes
# TODO: Commit all data to the database before quitting
dbcursor.close()
