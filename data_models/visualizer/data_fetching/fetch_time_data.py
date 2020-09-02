from django.db.models import Avg, Count
import json
from data_models.models import BBR
from redis import Redis
from data_store.settings import log

redis_client = Redis(host="redis")


def compute_time_data():
    log.info("Computing time data")
    return {"time": changes_over_time(), "rolling_avgs": get_rolling_avgs()}


def get_time_data():
    if redis_client.exists("time_graph_data"):
        log.info("Got time data from redis")
        return json.loads(redis_client.get("time_graph_data"))
    else:
        data = compute_time_data()
        redis_client.set("time_graph_data", json.dumps(data))
        return data


def _fill_zeroes(data):
    lower_val = 0
    for i in range(len(data)):
        lower_val = data[i] if data[i] > 0 else lower_val
        if data[i] == 0:
            upper_value = 0
            for j in range(i + 1, len(data)):
                if data[j] > 0:
                    upper_value = data[j]
                    break
            upper_value = upper_value if upper_value > 0 else lower_val
            data[i] = (upper_value + lower_val) / 2
    return data


def accumulated_sum_for_catatgorical(field, min_year, max_year):
    # TODO cache this?
    year_value = list(
        BBR.objects.values(field, "construction_year").order_by("construction_year")
    )
    result = []
    year = min_year
    keys = [val for (val, _name) in BBR._meta.get_field(field).choices]
    current_result = {key: 0 for key in keys}
    while len(year_value) > 0 and year <= max_year:
        if year != year_value[0]["construction_year"]:
            result.append(current_result.copy())
            year += 1
        else:
            value = year_value.pop(0)
            if value[field] is not None:
                current_result[value[field]] += 1

    result.append(current_result)
    return result


def changes_over_time():
    build_years = BBR.objects.values("construction_year").order_by("construction_year")
    min_year, max_year = (
        (
            build_years.first()["construction_year"],
            build_years.last()["construction_year"],
        )
        if len(build_years) > 0
        else (0, 0)
    )
    build_counts = {}
    for year in build_years.annotate(count=Count("construction_year")):
        build_counts[year["construction_year"]] = year["count"]

    recon_years = {}
    for year in BBR.objects.values("reconstruction_year").annotate(
        count=Count("reconstruction_year")
    ):
        recon_years[year["reconstruction_year"]] = year["count"]

    time_range = list(range(min_year, max_year + 1))
    build_cum_summed = []
    recon_cum_summed = []
    build_total = 0
    recon_total = 0
    for year in time_range:
        build_count = 0 if year not in build_counts.keys() else build_counts[year]
        build_total += build_count
        build_cum_summed.append(build_total)

        recon_count = 0 if year not in recon_years.keys() else recon_years[year]
        recon_total += recon_count
        recon_cum_summed.append(recon_total)

    return {
        "time_range": time_range,
        "houses_per_year": build_cum_summed,
        "recon_per_year": recon_cum_summed,
        "categorical": {
            "heat_install": accumulated_sum_for_catatgorical(
                "heat_install", min_year, max_year  # TODO is this right?
            )
        },
    }


def _compute_rolling_avgs(field, min_year, max_year):
    year_avgs = (
        BBR.objects.filter(**{field + "__gte": "0"})
        .values("construction_year")
        .annotate(Avg(field))
        .order_by("construction_year")
    )
    yearly_averages = {}
    for yearly_avg in year_avgs:
        yearly_averages[yearly_avg["construction_year"]] = yearly_avg[field + "__avg"]

    averages = []
    nr_year_rolls = 5
    for year in range(min_year, max_year + 1):
        lower_limit = ans if (ans := year - nr_year_rolls) >= min_year else min_year
        upper_limit = ans if (ans := year + nr_year_rolls) <= max_year else max_year
        to_roll = []
        for other_year in range(lower_limit, upper_limit + 1):
            if other_year in yearly_averages.keys():
                to_roll.append(yearly_averages[other_year])
        averages.append(sum(to_roll) / (ans if (ans := len(to_roll)) > 0 else 1))

    return _fill_zeroes(averages)


def get_rolling_avgs():
    build_years = BBR.objects.values("construction_year").order_by(
        "construction_year"
    )  # TODO pass as variable
    if len(build_years) == 0:
        min_year = 0
        max_year = 0
    else:
        min_year = build_years.first()["construction_year"]
        max_year = build_years.last()["construction_year"]

    return {
        "time_range": list(range(min_year, max_year + 1)),
        "bulding_area": _compute_rolling_avgs("building_area", min_year, max_year),
        "ground_area": _compute_rolling_avgs("ground_area", min_year, max_year),
        "roof_area": _compute_rolling_avgs("roof_area", min_year, max_year),
        "num_toilets": _compute_rolling_avgs("num_toilets", min_year, max_year),
        "num_rooms": _compute_rolling_avgs("num_rooms", min_year, max_year),
        "num_floors": _compute_rolling_avgs("num_floors", min_year, max_year),
        "garage_area": _compute_rolling_avgs("garage_area", min_year, max_year),
        "outhouse_area": _compute_rolling_avgs("outhouse_area", min_year, max_year),
    }
