"""Collect city and weather data of respective cities.

Uses (included in repository):
data/city.json.zip

Process:
1. Read cities ID list.
2. Request weather JSON data from openweathermap.org
3. Store/print significant weather data.

Format of output training data:

"""
import requests
import sys


def get_all_weather(key, cities_path, out=sys.stdout,
    err=sys.stderr, flush=True):
    """
    Get the current weather data of given cities file and print immediately
    to given output.
    :param key: API Key.
    :param cities_path: Path of the cities list file. Expects every line to
    consist only of a numerical ID of the city based off of openweathermap.
    :param out: Output file. Defaults to sys.stdout.
    :param flush: Flush flag. Defaults to True.
    :return: Count of city weather fetches.
    """
    with open(cities_path) as cfile:
        count = 0
        for row in cfile:
            # Fetch weather JSON for city by ID
            init_json = get_weather(format_request_url(row.rstrip(), key))
            # Process weather data
            if init_json != None:
                try:
	                weather_parent = init_json["weather"][0]
                except KeyError:
                    continue
                if "main" not in weather_parent:
                    print("no main, skip", flush=True)
                    continue # This dataset is useless; skip
                else:
                    weather = weather_parent["main"]

                main_parent = init_json["main"]
                if "pressure" not in main_parent\
                    or "temp" not in main_parent:
                    print("Doesnt have press or temp", flush=True)
                    continue # Also useless; skip
                else:
                    pressure = main_parent["pressure"]
                    temperature = main_parent["temp"]
                if "humidity" not in main_parent:
                    humidity = 0
                else:
                    humidity = main_parent["humidity"]

                if "wind" in init_json:
                    windspeed = init_json["wind"]["speed"]
                else:
                    windspeed = 0.0

                print(format_training_line(
                    weather=weather,
                    temp=temperature,
                    windspeed=windspeed,
                    humid=humidity,
                    pressure=pressure), flush=flush, file=out)
                count += 1
    return count


def get_weather(furl):
    """
    Get the weather of a city given API call.
    :param furl: URL of the API call.
    :return: JSON response with weather data.
    req = requests.get(furl)
    """
    req = requests.get(furl)
    return req.json()


def format_training_line(weather, temp, windspeed, humid, pressure) -> str:
    """
    Format to store and read later for training.
    :param weather: Weather description string.
    :param temp: Temperature float.
    :param windspeed: Wind speed.
    :param humid: Relative humidity percentage.
    :param pressure: Pressure.
    """
    return ",".join( # Convert each value into a string to join
        [str(x) for x in\
            [weather, temp, windspeed, humid, pressure]])


def format_request_url(cid, key, unit="metric") -> str:
    """
    Format for openweathermap API.
    :param cid: City ID.
    :param key: API Key.
    :return: Formatted URL string.
    """
    return "http://api.openweathermap.org/data/2.5/weather?id={}&units={}&APPID={}"\
        .format(cid, unit, key)

