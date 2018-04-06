"""Collect data and train the neural network.
"""
import argparse
import traceback

from city import get_all_weather
from model import Model
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
    metavar="TRAINING",
    help="train the model with given training data file path")
parser.add_argument("--seed",
    type=int,
	default=7,
    help="Set the random generator seed")
parser.add_arugment("--epochs",
	type=int,
	default=150,
	help="number of epochs for training")
parser.add_argument("--batch-size",
	type=int,
	default=10,
	help="batch size for training")
args = parser.parse_args()

# Collect
if args.collect and args.key:
    c = get_all_weather(args.key, cities_path=args.collect)
    print("TOTAL FETCHES: {}".format(c))
    quit()
elif args.train: # Train the NN
    mod = Model(training=args.train, seed=args.seed)
    mod.train(training=args.train,
		batch_size=args.batch_size,
		epochs=args.epochs)
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

