"""List all the unique weather conditions in given training data file.

Assumes the first value of each line (split by ',') is the condition string.
"""
import sys


def find_all_conditions(path: str) -> set:
    """
    Find all unique conditions in given training data file.
    :param path: Path to training data.
    :return: Set of all the unique available conditions in the file.
    """
    cond = set()
    with open(path) as f:
        for line in f:
            split = line.split(",")
            if len(split) >= 1: # Don't have to be strict about the format
                try: # If it's a number, don't add to the set
                    float(split[0])
                except ValueError:
                    # Not a number, add to set if not already in it
                    if split[0] not in cond:
                        cond.add(split[0])
    return cond


def find_from_iterable(it) -> set:
    """
    Find all unique conditions in given iterable object.
    :param it: Iterable object to traverse.
    :return Set of all unique available conditions.
    """
    cond = set()
    for i in it:
        if i not in cond:
            cond.add(i)
    return cond


def from_file(path: str) -> set:
    """
    Read conditions from a file. Each line contains a separate condition.
    :param path: Path to file.
    :return: Read conditions.
    """
    conditions = set()
    with open(path) as f:
        for line in f:
            conditions.add(line)
    return conditions


def to_dict(condset: set) -> dict:
    """
    Create a dictionary of conditions with a unique integer value for each
    condition.
    :param condset: Conditions set.
    :return: Dictionary of all conditions with integer values.
    """
    conds = {}
    index = 0
    for item in condset:
        conds[str(item)] = index
        index += 1
    return conds


def print_conditions(cond: set, output=sys.stdout):
    """
    Print all conditions in the given set.
    :param cond: Set of conditions.
    :param output: Output destination. Default is sys.stdout.
    """
    for c in cond:
        print(c, flush=True, file=output)
