import json
import os


def get_test_addresses():
    path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(path, "test_addresses.json"), "r") as data:
        data = json.loads(data.read())
    return data
