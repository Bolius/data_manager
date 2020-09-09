import json
import os

import requests
import utm
from django.conf import settings

header = {"Authorization": "Basic " + os.environ["GEO_KEY"]}


def _getAddressInfo(address):
    """Url : apps.conzoom.eu/api/v1/values/dk/unadr/21370905?apikey=KEY."""
    baseUrl = "https://apps.conzoom.eu/api/v1/match/dk/geocoder?in_adr="
    address = address.replace(" ", "%20")
    configs = "&" + "apikey=" + settings.GEO_KEY
    req = baseUrl + address + configs
    return requests.get(req).json()


def _getExtendedInfo(match):
    """Url : apps.conzoom.eu/api/v1/values/dk/unadr/21370905?apikey=KEY."""
    if match is not None:  # or match['match'] is None:
        req = match["match"]["self"]["url"] + "?" + "apikey=" + settings.GEO_KEY
        return requests.get(req).json()
    return {"error", "No house"}


def _getBBRInfo(match):
    """Url : apps.conzoom.eu/api/v1/values/dk/unit/b6c20cff-8399-4591-934c-
    6774354f068a?apikey=9a8cfab82206e05083dbd1112adc06d5.
    """
    unadr = str(match["values"]["unadr_key"])
    req = "https://apps.conzoom.eu/api/v1/values/dk/unit?where=unadr_key="
    req += unadr + "&apikey=" + settings.GEO_KEY
    buldings = requests.get(req).json()
    if len(buldings["objects"]) == 0 or len(buldings["objects"][0]) == 0:
        return {}

    req = buldings["objects"][0]["self"]["url"] + "?apikey=" + settings.GEO_KEY
    return requests.get(req).json()


def _getPropValue(bbid):
    """Url : https://dingeologi.appspot.com/_ah/api/boliusendpoint/v1/stam?
    addressUnitId=40eb1f85-9c53-4581-e044-0003ba298018"""
    base = "https://dingeologi.appspot.com/_ah/api/boliusendpoint/v1/stam?"
    req = base + "addressUnitId=" + bbid
    keys = ["ejendomsvaerdi", "grundvaerdi", "ejendomstype"]
    resp = requests.get(req)
    resp = resp.json() if resp.status_code == 200 else {}
    output = {"ejendomsvaerdi": -1}
    for key in keys:
        output[key] = resp[key] if key in resp.keys() else None
        output = None if output["ejendomsvaerdi"] == -1 else output
    return output


def addressToJson(address):
    """Combine all api calls and returns a JSON obejct."""
    data = _getAddressInfo(address)
    data["output"] = {}
    address = _getExtendedInfo(data)
    bbrInfo = _getBBRInfo(address)
    data["output"]["BBR"] = bbrInfo
    data["output"]["info"] = address
    data["money"] = _getPropValue(data["output"])
    return json.dumps(data)


def addressToKVH(address):
    url = "https://apps.conzoom.eu/api/v1/match/dk/geocoder?in_adr=" + address
    return requests.get(url, headers=header).json()["match"]["values"]["kvh"]


def addresToGroundType(address, GTData):
    url = "https://apps.conzoom.eu/api/v1/match/dk/geocoder?in_adr=" + address
    x = requests.get(url, headers=header).json()["match"]["values"]["kvh"]["acadr_loc"][
        "x"
    ]
    y = requests.get(url, headers=header).json()["match"]["values"]["kvh"]["acadr_loc"][
        "y"
    ]

    # Convert x and y to lon and lat
    x, y = utm.to_latlon(x, y, 32, "U")

    # keep the ones where xmin is smaller than p.x
    geo_data_reduced = GTData[GTData["minx"] <= x]

    # filter out the ones where xmax is smaller than p.x
    geo_data_reduced = geo_data_reduced[geo_data_reduced["maxx"] > x]

    # keep the ones where ymin is smaller than p.y
    geo_data_reduced = geo_data_reduced[geo_data_reduced["miny"] <= y]

    # filter out the ones where ymax is smaller than p.y
    geo_data_reduced = geo_data_reduced[geo_data_reduced["maxy"] > y]

    geo_data_reduced = geo_data_reduced["minx"] - x

    closest = abs(geo_data_reduced).sort_values().index

    for poly in closest:
        if GTData.loc[poly].geometry.contains((x, y)):
            return poly
    return "unknown type"


def kvhToBBR(kvh):
    req = "https://apps.conzoom.eu/api/v1/values/dk/unit/?where=kvh%3D" + kvh
    url = requests.get(req, headers=header).json()["objects"][0]["self"]["url"]
    data = requests.get(url, headers=header).json()
    bbrid = data["values"]["unadr_bbrid"]
    return {"bbr": data, "money": _getPropValue(bbrid)}
