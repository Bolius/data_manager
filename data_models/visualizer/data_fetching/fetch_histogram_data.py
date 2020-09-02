import json

from redis import Redis

from data_models.models import Municipality
from data_store.settings import log

from .fetch_municipality_map import get_municipality_data

redis_client = Redis(host="redis")


def get_histogram_data():
    if redis_client.exists("hist_graph_data"):
        log.info("Got Hist data from redis")
        return json.loads(redis_client.get("hist_graph_data"))
    else:
        data = compute_histogram_data()
        log.info("Computed Hist graph data")
        redis_client.set("hist_graph_data", json.dumps(data))
        return data


def compute_histogram_data():
    municipalites = get_municipality_data()["categorical"]
    return {
        "municipalities": list(Municipality.objects.all().values("name", "admin_code")),
        "municipalities_categories": {
            muni: convert_to_percentage(municipalites[muni]) for muni in municipalites
        },
        "denmark": convert_to_percentage(
            combine_categoricals_to_denmark(municipalites)
        ),
    }


def combine_categoricals_to_denmark(municipalities):
    denmark = {}
    for muni in municipalities:
        for categori in municipalities[muni]:
            if categori not in denmark.keys():
                denmark[categori] = {}
            for field in municipalities[muni][categori]:
                # Ewww triple for loop, but we cache it.
                if field not in denmark[categori]:
                    denmark[categori][field] = 0

                denmark[categori][field] += municipalities[muni][categori][field]
    return denmark


def convert_to_percentage(muni):
    for category in muni:
        total = sum(muni[category].values())
        for field in muni[category]:
            muni[category][field] = (
                round(muni[category][field] / total * 100, 2) if total > 0 else 0
            )
    return muni
