"""Print all city IDs.

Modify PATH if necessary.
"""
import sys


PATH = "data/openweathermap.txt"

with open(PATH) as f:
    for line in f:
        parse = line.split(maxsplit=1)
        if parse[0] != "id":
            print(parse[0], flush=True)


