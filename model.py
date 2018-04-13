"""The model to be trained
"""
import numpy
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.utils import to_categorical

from conditions import find_from_iterable, to_dict
from verify import COLUMNS


class WeatherGuessModel:
    """
    Set up and use the model for training/evaluation...
    """

    def __init__(self, training: str, seed: int):
        """
        :param seed: Generator seed to use with numpy.random.
        :param training: Path to training data file.
        """
        numpy.random.seed(seed)
        self.training = training

    def _setup(self):
        """
        Build and compile the Keras model.
        """
        print("Setting up model..")
        # Build model
        self.model = Sequential()
        self.model.add(Dense(100, activation="relu", input_shape=(4,)))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(50, activation="relu"))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(360, activation="relu"))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(50, activation="relu"))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(13, activation="softmax"))

        self.model.summary()
        self.model.save("weatherguess.h5")
        # plot_model(self.model, to_file="weatherguess_model.png")

        print("Compiling model...")
        self.model.compile(loss="sparse_categorical_crossentropy",
                           optimizer="rmsprop",
                           metrics=["accuracy"])

    def _train(self, x, y, epochs=150, batch_size=32):
        """
        Train the model.
        :param x: Input variable.
        :param y: Output variable.
        :param epochs:
        :param batch_size:
        """
        # Fit
        return self.model.fit(x, y,
                       epochs=epochs,
                       batch_size=batch_size,
                       verbose=1)

    def perform(self, epochs, batch_size):
        """
        Train and evaluate the model.
        """
        x, y = _get_variables(self.training)
        print("x = {}".format(x), "\ny = {}".format(y))
        print("x input shape: {}".format(x.shape))
        print("y output shape: {}".format(y.shape))
        self._setup()
        results = self._train(x, y, epochs, batch_size)


def _get_variables(training: str):
    """
    Get the x (input) and y (output) from training data.
    :param training: Path to training data file.
    :return: X and Y.
    """
    data = numpy.genfromtxt(training,
                            delimiter=",",
                            dtype=("|U18", numpy.float64, numpy.float64, numpy.float64, numpy.float64),
                            names=COLUMNS,
                            encoding=None)
    # Assign to input/output variables
    pre_x = data[list(COLUMNS[1::])]  # Every other field is input
    pre_y = data[COLUMNS[0]]  # Weather condition is our output (first index)

    # Formatting/encoding/etc
    all_conds = to_dict(find_from_iterable(set(pre_y)))
    print("all_conds = ", all_conds)
    y = [all_conds[item] for item in pre_y]
    # y = to_categorical(y, num_classes=len(all_conds))
    x = [list(nx) for nx in pre_x]
    return numpy.array(x), numpy.array(y)
