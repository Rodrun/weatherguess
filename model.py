"""The model to be trained
"""
from keras.models import Sequential
from keras.layers import Dense
import numpy

from verify import COLUMNS


class Model:
    """
    Set up and use the model for training/evaluation...
    """
    __model = None # Keras model
    __x = None # Input
    __y = None # Output


    def __init__(self, training: str, seed: int):
        """
        :param seed: Generator seed to use with numpy.random.
        :param training: Path to training data file.
        """
        numpy.random.seed(seed)
        setup()


    def setup(self):
        """
        Build and compile the Keras model.
        """
        print("Setting up model..")
        # Build model
        __model = Sequential()
        __model.add(Dense(6, input_dim=5, activation="relu"))
        __model.add(Dense(4, activation="relu"))
        __model.add(Dense(1, activation="softmax"))
        # Compile model
        print("Compiling model...")
        __model.compile(loss="categorical_crossentropy",
            optimizer="adam",
            metrics=["accuracy"])


    def get_variables(self, training: str):
        """
        Get the x (input) and y (output) from training data.
        :param training: Path to training data file.
        :return: X and Y.
        """
        data = numpy.genfromtxt(training,
            delimiter=",",
            dtype=None,
            names=COLUMNS)
        # Assign to input/output variables
        y = data[COLUMNS[0]] # Weather condition is our output
        x = data[list(COLUMNS[1::])] # Every other field is input
        return x, y


    def train(self, training: str, epochs=150, batch_size=10):
        """
        Train the model.
        :param epochs:
        :param batch_size:
        :param training: Path to training data file.
        """
        # Read data
        x, y = get_variables(training)
        # Fit
        __model.fit(x, y, epochs=epochs, batch_size=batch_size)

