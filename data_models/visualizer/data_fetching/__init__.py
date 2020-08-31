from .fetch_municipality_map import get_municipality_data
from .fetch_time_data import (
    accumulated_sum_for_catatgorical,
    get_rolling_avgs,
    get_time_data,
)

__all__ = [
    "accumulated_sum_for_catatgorical",
    "get_rolling_avgs",
    "get_time_data",
    "get_municipality_data",
]


def fill_redis():
    get_municipality_data()
