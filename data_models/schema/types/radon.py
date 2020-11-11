import json
import os
import pickle

import pandas as pd
import requests

with open("encoder.model", "rb") as e:
    e = pickle.load(e)
with open("scalar.model", "rb") as s:
    s = pickle.load(s)
with open("clf.model", "rb") as c:
    c = pickle.load(c)


def kvhxToRadon(kvhx):
    data = kvhxToSeries(kvhx=kvhx)
    encoded = encodeVals(data)
    return predict(encoded)[0]


def predict(ser):
    ser.resityp_geo = e.transform([ser.resityp_geo])
    ser = s.transform([ser])
    return c.predict(ser)


def kvhxToSeries(kvhx=None):
    coords = "latlong"
    url = "https://apps.conzoom.eu/api/v1"
    print(f'Basic {os.environ["API_KEY"]}')
    header = {"authorization": f'Basic {os.environ["API_KEY"]}'}
    response = requests.request(
        "GET",
        f"{url}/match/dk/geocoder",
        headers=header,
        params={"in_kvhx": kvhx},
    )
    if response.status_code != 200:
        raise ValueError("Non '200' return code from bbr")
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
        raise ValueError("Non '200' return code from bbr on bulding")
    bld_data = json.loads(bld_data.content)
    return bld_data["values"]


def encodeVals(vals):
    return pd.Series(
        {
            "zip": int(vals["pcode"]),
            "has_basement": 0 if vals["bld_area_basement"] is None else 1,
            "floors": vals["bld_floors"],
            "kommune_id": int(vals["muni"]),
            "build_year": int(vals["bld_conyear"].split("-")[0]),
            "rebuild_year": (
                int(vals["bld_reconyear"].split("-")[0])
                if vals["bld_reconyear"] is not None
                else 0
            ),
            "area_resi": vals["bld_area_resi"],
            "area_basement": (
                0 if vals["bld_area_basement"] is None else vals["bld_area_basement"]
            ),
            "resityp_geo": vals["unit_resityp_geo"],
            "rooms": vals["unit_rooms"],
        }
    )
