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

# TODO: Simple CMD interface to manually add to the DB the data that we wish
# Available input options:
# - A location name, e.g. "Kvevlax, Finland", to search a location and add or update its weather data in the database
# - "#view" to display the database in its entirety
# - "#clear" to clear the whole database
# - "#quit" to quit the program

while True:
    inputline = input("> ")
    
    print() # output spacer

    if not(inputline.startswith("#")): # If line doesn't start with a #, treat user's input as the plaintext name of the location that we must get the weather information for

        # URL encode the location's plaintext name (e.g. "Kvevlax, Finland" must become "Kvevlax%2C+Finland").
        location_urlencoded = urllib.parse.urlencode({'' : inputline})[1:] # en fuling? Turns e.g. "=Kvevlax%2C+Finland" into just "Kvevlax%2C+Finland"

        # Query OpenWeatherMap Geocoding API to get geographical coordinates for the location        
        # Ask only for the very first match and assume that it is the correct location that the user wanted ("&limit=1")
        request_string_geocoding = "http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={appid}".format(location=location_urlencoded, appid=API_KEY)

        try:
            geocoding_response = urllib.request.urlopen(request_string_geocoding).read().decode() # read the whole API response # the returned object works like an "fhand"
        except Exception as err:
            print("Error while requesting geocoding data - ", err)
            continue

        geocoding_data = json.loads(geocoding_response) # returns a dictionary

        print(geocoding_data[0]["name"]) # debug prints
        print(geocoding_data[0]["lat"])
        print(geocoding_data[0]["lon"])
        print(geocoding_data[0]["country"])

        lat = geocoding_data[0]["lat"]
        lon = geocoding_data[0]["lon"]

        print() # output spacer

        # Query the OpenWeatherMap One Call 3.0 API to get the weather data for the location
        # 
        request_string_weather = "https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily,alerts&units=metric&appid={appid}".format(lat=lat, lon=lon, appid=API_KEY)

        try:
            weather_response = urllib.request.urlopen(request_string_weather).read().decode() # read the whole API response # the returned object works like an "fhand"
        except Exception as err:
            print("Error while requesting weather data - ", err)
            continue

        weather_data = json.loads(weather_response) # returns a dictionary

        print(weather_data["timezone"]) # debug prints
        print(weather_data["current"]["temp"], "degrees celsius")
        print(weather_data["current"]["weather"][0]["description"])

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
