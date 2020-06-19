import json
import os

import requests


def getBBRInfo(address=None, kvhx=None, coords="latlong"):
    if address is None and kvhx is None:
        raise ValueError("No Input specified")
    url = "https://apps.conzoom.eu/api/v1"
    header = {"authorization": f'Basic {os.environ["GEO_KEY"]}'}
    response = requests.request(
        "GET",
        f"{url}/match/dk/geocoder",
        headers=header,
        params={"in_adr": address} if kvhx is None else {"in_kvhx": kvhx},
    )
    if response.status_code != 200:
        raise ValueError("Non '200' return code from geomatic")

    data = json.loads(response.content)
    if data["match"] is None or data["matchinfo"]["unadr_matchlvl"] in ["x", "i"]:
        raise ValueError("No address found")
    bld_data = requests.request(
        "GET",
        f"{url}/values/dk/unit/{data['match']['values']['unadr_primunit_key']}",
        headers=header,
        params={"coords": coords},
    )
    if bld_data.status_code != 200:
        raise ValueError("Non '200' return code from geomatic on bulding")
    bld_data = json.loads(bld_data.content)

    return bld_data["values"]
