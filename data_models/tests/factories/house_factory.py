from random import randint

import requests
from tqdm import tqdm

from data_models.models import House


def add_houses(nr_houses=100, page_nr=None):
    if page_nr is None:
        page_nr = randint(1, 190)
    response = requests.request(
        "GET",
        "https://dawa.aws.dk/bbrlight/enheder",
        params={
            "per_side": nr_houses,
            "side": randint(1, 250),
            "anvendelseskode": "120",
        },
    )
    created_houses = []
    for house_bulding in tqdm(response.json(), desc="Adding houses"):
        created_houses.append(House.add_house_by_access_id(house_bulding["EnhAdr_id"]))
    return created_houses
