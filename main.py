"""Collect data and train the neural network.
"""
import argparse
import traceback
import sys

from city import format_request_url, get_weather
from collection import Collection
from model import WeatherGuessModel
import conditions
import verify

# Setup argument parser
parser = argparse.ArgumentParser(
    description="Weather guessing neural network experiment")
parser.add_argument("-k", "--key",
                    type=str,
                    help="openweathermap.org API key.")
parser.add_argument("-c", "--collect",
                    type=str,
                    metavar="CITIES",
                    help="collect weather data from given cities list file path and exit")
parser.add_argument("--verify",
                    nargs=2,
                    metavar=("TRAINING", "CONDITIONS"),
                    help="verify collected training data. Takes path to training data" \
                         + " and path to weather condition list file")
parser.add_argument("--get-conditions",
                    nargs=2,
                    metavar=("TRAINING", "OUTPUT"),
                    help="get all the weather conditions present in training data file")
parser.add_argument("-t", "--train",
                    type=str,
                    metavar="TRAINING",
                    help="train the model with given training data file path")
parser.add_argument("--seed",
                    type=int,
                    default=7,
                    help="Set the random generator seed")
parser.add_argument("--epochs",
                    type=int,
                    default=150,
                    help="number of epochs for training")
parser.add_argument("--batch-size",
                    type=int,
                    default=32,
                    help="batch size for training")
args = parser.parse_args()

# Collect
if args.collect and args.key:
    # get_all_weather(args.key, cities_path=args.collect)
    # Read city ID list file
    with open(args.collect) as f:
        collector = Collection()
        for cid in f:
            url = format_request_url(cid.rstrip(), args.key)
            wdat = get_weather(url)
            data = [str(x) for x in collector.get_weather(wdat)]
            print(verify.format_line(data), flush=True)
elif args.train:  # Train the NN
    mod = WeatherGuessModel(training=args.train, seed=args.seed)
    mod.perform(batch_size=args.batch_size, epochs=args.epochs)
else:
    # Get conditions
    if args.get_conditions:
        try:
            with open(args.get_conditions[1], "w+") as output:
                conditions.print_conditions(
                    conditions.find_all_conditions(args.get_conditions[0]),
                    output)
        except OSError as oerr:
            print("OSError occurred opening OUTPUT file: {}".format(oerr))
            traceback.print_exc()
    # Verify
    if args.verify:
        verify.verify_file(args.verify[0],
                           conditions.from_file(args.verify[1]))
