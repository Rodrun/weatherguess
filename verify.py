"""Verify training data.

Format:
condition,temperature,wind speed,relative humidity,pressure
"""
import argparse
import conditions

COLUMNS = ("condition", "temperature", "wind_speed", "relative_humidity",
           "pressure")


def verify_line(line: str, no: int, conds: set):
    """
    Verify if the given line is compliant to the training data format.
    :param line: Line string.
    :param no: Line number.
    :param conds: Available weather condition strings.
    :return: Faulty line number, otherwise None.
    """
    if conds is None:
        return None
    # Test 1: has the correct amount of values? (5)
    split = line.split(",")
    if len(split) != 5:
        return no
    else:
        # Test 2: each value the right type?
        if split[0].lower() not in conds:  # Must be condition
            return no
        for i in range(1, len(split)):  # The rest of the values
            try:
                float(split[i])
            except ValueError:  # Must be numbers
                return no
    return None


def verify_file(path: str, cond: set):
    """
    Verify an entire training data file.
    :param path: Path to training data file.
    :param cond: Set of weather conditions available.
    """
    faulty = []
    record = None
    with open(path) as f:
        count = 1
        # Read
        record = f.readlines()
        for line in f:
            ver = verify_line(line, count, cond)
            if ver is not None:
                faulty.push(ver)
            count += 1

    if len(faulty) > 0:
        count = 1
        # List should already be sorted naturally
        # will keep track of which index of faulty should be checked.
        current_index = 0

        with open(path + "-verified", 'w') as f:
            for line in record:
                if count != len(faulty) and faulty[current_index] == count:
                    current_index += 1
                else:
                    f.write(line)
                if current_index < len(faulty):
                    count += 1
