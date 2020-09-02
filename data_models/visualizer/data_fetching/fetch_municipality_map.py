import json

import pandas as pd
from django.db.models import Avg, Count
from redis import Redis

from data_models.models import BBR, House, Municipality
from data_store.settings import log

redis_client = Redis(host="redis")


def get_municipality_data():
    if redis_client.exists("municipality_map_data"):
        log.info("Fetching municipality data from redis")
        stats = json.loads(redis_client.get("municipality_map_data"))
        stats["muni_averages"] = pd.read_json(stats["muni_averages"])
        stats["data"] = pd.read_json(stats["data"], dtype={"admin_code": str})
        stats["data"].index = stats["data"]["admin_code"]
        log.info("GOT DATA FROM REDIS")
        return stats
    else:
        stats = compute_stats()
        log.info("GOT DATA FROM REDIS")
        data = {
            "data": stats["data"].to_json(),
            "categorical": stats["categorical"],
            "muni_averages": stats["muni_averages"].to_json(),
        }
        redis_client.set("municipality_map_data", json.dumps(data))
        return stats


def compute_stats():
    log.info("Computing municipality map data")
    res = {
        "data": [],
        "categorical": {},
    }
    municipalities = Municipality.objects.all()
    muni_averages = []
    for municipality in municipalities:
        buldings_in_muni = BBR.objects.filter(
            accsses_address__municipality=municipality
        )
        averages = buldings_in_muni.aggregate(
            *[Avg(int_field) for int_field in BBR.integer_fields]
        )
        res["data"].append(
            {
                "admin_code": municipality.admin_code,
                "name": municipality.name,
                "nr_houses": House.objects.filter(municipality=municipality).count(),
            }
        )
        muni_averages.append(averages)
        res["categorical"][municipality.admin_code] = {}
        for cat_field in BBR.categorical_fields:
            choices = [
                field.choices for field in BBR._meta.fields if field.name == cat_field
            ][0]
            res["categorical"][municipality.admin_code][cat_field] = {}
            for val, _name in choices:
                res["categorical"][municipality.admin_code][cat_field][val] = 0

            counts = buldings_in_muni.values(cat_field).annotate(count=Count(cat_field))
            for c in counts:
                try:
                    res["categorical"][municipality.admin_code][cat_field][
                        c[cat_field]
                    ] += c["count"]
                except KeyError as e:
                    # TODO setup sentry                        capture_exception(e)
                    #                        capture_message(f"Key error For field {cat_field}")
                    print(e)
                    print(f"Key error For field {cat_field}")
                    continue
    res["muni_averages"] = pd.DataFrame(muni_averages)
    res["data"] = pd.DataFrame(res["data"])
    res["data"].index = res["data"]["admin_code"]
    return res
