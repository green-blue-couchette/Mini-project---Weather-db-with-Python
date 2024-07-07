#!/usr/bin/python3

# Author: O.A.

# A simple app that saves location and weather data into a SQLite database and displays it

import sqlite3

# Create database
dbconnnection = sqlite3.connect('weatherdb.sqlite'); # creates database on disk, in the directory from where this program is invoked.
dbcursor = dbconnnection.cursor()

# Set up database tables
dbcursor.executescript('''
DROP TABLE IF EXISTS Place;
DROP TABLE IF EXISTS Country;
DROP TABLE IF EXISTS Weather_status;

CREATE TABLE Place (
    "id"	INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
    "Name"	TEXT NOT NULL,
	"Country_id"	INTEGER NOT NULL,
	"Weather_status_id"	INTEGER NOT NULL
);

CREATE TABLE Country(
	"id"	INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
	"Name"	TEXT NOT NULL UNIQUE
);

CREATE TABLE Weather_status(
    "id"    INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
    "Status" TEXT NOT NULL UNIQUE 
);
''')

### First version: Populate the database with some example data
dbcursor.executescript('''
INSERT OR IGNORE INTO Country (Name) VALUES ("Sweden");
INSERT OR IGNORE INTO Country (Name) VALUES ("Germany");
INSERT OR IGNORE INTO Country (Name) VALUES ("Hungary");
INSERT OR IGNORE INTO Country (Name) VALUES ("Romania");
''')

dbcursor.executescript('''
INSERT INTO Weather_Status (Status) VALUES ("Sunny");
INSERT INTO Weather_Status (Status) VALUES ("Partly cloudy");
INSERT INTO Weather_Status (Status) VALUES ("Overcast");
INSERT INTO Weather_Status (Status) VALUES ("Gentle rain");
INSERT INTO Weather_Status (Status) VALUES ("Heavy rain");
INSERT INTO Weather_Status (Status) VALUES ("Mist");
''')

dbcursor.executescript('''
INSERT INTO PLACE (Name, Country_id, Weather_status_id) VALUES ("Nacka", "1", "1");
INSERT INTO PLACE (Name, Country_id, Weather_status_id) VALUES ("Sollentuna", "1", "2");
INSERT INTO PLACE (Name, Country_id, Weather_status_id) VALUES ("Székesfehérvár", "3", "3");
INSERT INTO PLACE (Name, Country_id, Weather_status_id) VALUES ("Csengersima", "4", "5");
INSERT INTO PLACE (Name, Country_id, Weather_status_id) VALUES ("Karlsberg", "1", "6");
INSERT INTO PLACE (Name, Country_id, Weather_status_id) VALUES ("Matricahely", "3", "1");
INSERT INTO PLACE (Name, Country_id, Weather_status_id) VALUES ("Baia Mare", "4", "1");
INSERT INTO PLACE (Name, Country_id, Weather_status_id) VALUES ("Karlsruhe", "2", "2");
''')

dbconnnection.commit()

# Display all the data in the database in JOINed fashion
selectstring = '''SELECT Place.Name, Country.Name, Weather_Status.Status FROM Place
JOIN Country on Place.Country_id=Country.id
JOIN Weather_Status on Place.Weather_status_id=Weather_status.id;
'''

for row in dbcursor.execute(selectstring):
    for item in row:
        print(item, end='\t')
    print()

# TODO: Simple CMD interface to manually add to the DB the data that we wish

# TODO: Retrieve weather data from OpenWeatherMap and add it to the database

# Program finishes
dbcursor.close()
