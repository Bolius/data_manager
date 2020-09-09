from django.db.models import Count

from data_models.models import BBR


def get_scatter_data():
    return compute_scatter_data()


def compute_scatter_data():
    data = {}
    for int_field in BBR.integer_fields:
        data[int_field + "s"] = list(
            BBR.objects.values(int_field)
            .order_by(int_field)
            .annotate(count=Count(int_field))
        )
    return data
