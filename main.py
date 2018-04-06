"""Collect data and train the neural network.
"""
from city import get_all_weather
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-k", "--key",
    type=str,
    help="openweathermap.org API key.")
parser.add_argument("-c", "--collect",
    type=str,
    help="collect weather data from given cities list file path")
parser.add_argument("-t", "--train",
    type=str,
    help="train the model with given training data file path")
args = parser.parse_args()
# In order: collect, train, evaluate?, predict

# Collect
if args.collect and args.key:
    c = get_all_weather(args.key, cities_path=args.collect)
    print("TOTAL FETCHES: {}".format(c))

