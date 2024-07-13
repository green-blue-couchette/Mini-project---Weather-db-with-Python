# About "Mini project - Weather DB with Python 3"
A simple personal project where I tie together some basic knowledge from Python 3 and SQLite databases, which I learned on my free time.

## What it is
A small command-line program that lets you search for a location, e.g. `Kvevlax, Finland`, and store its current weather info from OpenWeatherMap in an SQLite database. It also lets you view or delete the stored places and their weather data afterwards.

## How to use
Download the `weatherdb.py` and `credentials.py` scripts to your machine.\
Run it using `python3 weatherdb.py` or `./weatherdb.py`. Make sure you fill the credentials file with your own OpenWeatherMap API key first.

If this is the first time you run `weatherdb.py`, enter the command `#clear` at the prompt to create the `.sqlite` database. Otherwise, you will get an error.


## Libraries and tools used
Python 3 for the programming language,\
Visual Studio Code for writing the code,\
[Postman](https://www.postman.com/) to get acquainted with OpenWeatherMap's REST API endpoint's responses, \
[SQLite](https://www.sqlite.org/index.html) and the [DB Browser for SQLite](https://sqlitebrowser.org/) for the database.

The python script uses the libraries `sqlite 3` for the database operations, and `urllib` and `json` for making REST API requests and parsing the responses.

## Screenshots
Searching for a location, e.g. `Köln`:
![Location search example output](https://github.com/user-attachments/assets/2fe9ab46-1824-41af-bbf5-ff5ecd6a17be)

Displaying all searched locations that got stored in `weatherdb.sqlite` - SQLite DB browser's contents vs `weatherdb.py`'s output:
![Python 3 output and SQLite DB example output](https://github.com/user-attachments/assets/d7b8cca7-0600-4450-acf6-84eab931deb4)
