"""Collect data and train the neural network.
"""
import argparse
import traceback

from city import get_all_weather
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
    help="verify collected training data. Takes path to training data"\
        + " and path to weather condition list file")
parser.add_argument("--get-conditions",
    nargs=2,
    metavar=("TRAINING", "OUTPUT"),
    help="get all the weather conditions present in training data file")
parser.add_argument("-t", "--train",
    type=str,
    metavar="training",
    help="train the model with given training data file path")
args = parser.parse_args()
# In order: collect, verify, train, evaluate?, predict


# Collect
if args.collect and args.key:
    c = get_all_weather(args.key, cities_path=args.collect)
    print("TOTAL FETCHES: {}".format(c))
    quit()
elif False:
    pass
else:
    # Get conditions
    if args.get_conditions:
        try:
            with open(args.get_conditions[1], "w+") as output:
                conditions.print_conditions(
                    conditions.find_all_conditions(args.get_conditions[0]),
                    output)
        except OSError as oerr:
            print("OSError occured opening OUTPUT file: {}".format(oerr))
            traceback.print_exc()
    # Verify
    if args.verify:
        verify.verify_file(args.verify[0],
            conditions.from_file(args.verify[1]))

