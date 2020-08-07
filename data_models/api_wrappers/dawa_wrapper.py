import requests


def address_to_kvhx(address):
    response = requests.request(
        "GET", "https://dawa.aws.dk/adresser", params={"q": address}
    )
    if response.status_code != 200:
        raise ValueError(f"Dawa gave error: {response.status_code} for {address=}")
    response = response.json()
    if len(response) == 0:
        raise ValueError(f"Dawa gave empty list for {address=}")
    return response[0]["kvhx"]


def kvhx_to_address(kvhx, small_resp=False):
    response = requests.request(
        "GET",
        "https://dawa.aws.dk/adresser",
        params={"kvhx": kvhx, "struktur": "mini" if small_resp else "nestet"},
    )
    if response.status_code != 200:
        raise ValueError(f"KVHX ({kvhx}) not found")
    data = response.json()
    if len(data) != 1:
        raise ValueError(f"Found multiple addresses for {kvhx=}")
    return data[0]


def access_id_to_address(access_id, small_resp=False):
    response = requests.request(
        "GET",
        f"https://dawa.aws.dk/adresser/{access_id}",
        params={"struktur": "mini" if small_resp else "nestet"},
    )
    if response.status_code != 200:
        raise ValueError(f"({access_id=}) not found")
    return response.json()


def dawa_id_to_bbr(dawa_id):
    response = requests.request(
        "GET", "https://dawa.aws.dk/bbrlight/enheder", params={"adresseid": dawa_id},
    )
    if response.status_code != 200:
        raise ValueError(f"DAWA ID {dawa_id} not found")

    return response.json()


def get_buildings_from_address_id(address_id):
    # TODO USE https://dawa.aws.dk/bbrlight/enheder?adresseid=40eb1f85-9c53-4581-e044-0003ba298018
    # Instead
    response = requests.request(
        "GET",
        "https://dawa.aws.dk/bbrlight/enheder",
        params={"adgangsadresseid": address_id},
    )
    if response.status_code != 200:
        raise ValueError(f"{address_id=} not found")
    ground_id = response.json()[0]["Bygning_id"]

    response = requests.request(
        "GET", "https://dawa.aws.dk/bbrlight/bygninger", params={"id": ground_id},
    )
    if response.status_code != 200:
        raise ValueError(f"{ground_id=} not found")
    return response.json()
