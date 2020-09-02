from .fetch_histogram_data import get_histogram_data
from .fetch_municipality_map import get_municipality_data
from .fetch_time_data import (
    accumulated_sum_for_catatgorical,
    compute_time_data,
    get_time_data,
)

__all__ = [
    "accumulated_sum_for_catatgorical",
    "get_time_data",
    "get_municipality_data",
    "compute_time_data",
    "get_histogram_data",
]


def fill_redis():
    get_municipality_data()
    get_time_data()
    get_histogram_data()
