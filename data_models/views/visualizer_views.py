# from django.core.management import call_command
from django.core.management import call_command
from django.shortcuts import render

from data_models.models import House, BBR


def has_migrated():
    """ A dirty hack around plotly loading apps before migrations are applied """
    # TODO Make a better way for this
    with open("/tmp/migrate_status", "w") as f:
        call_command("showmigrations", stdout=f)
    with open("/tmp/migrate_status", "r") as f:
        lines = " ".join(f.readlines())
    return "[ ]" not in lines


if has_migrated():
    from data_models.visualizer import (  # noqa
        HISTOGRAM_GRAPH,
        MAP_GRAPH,
        MUNICIPALITY_GRAPH,
        SCATTER_GRAPH,
        TIME_GRAPH,
    )


def scatter(request):
    return render(request, "data_models/scatter.html")


def TimeView(request):
    return render(request, "data_models/time.html")


def map(request):
    return render(request, "data_models/map.html")


def MunicipalityMapView(request):
    return render(request, "data_models/municipality_map.html")


def HistogramView(request):
    return render(request, "data_models/histogram.html")


def address_enter(request):
    return render(request, "data_models/adressView.html", {})


def address_view(request, address_id=None):
    if address_id is None:
        return render(request, "data_models/adressView.html", {})
    else:
        house = House.add_house(access_id=address_id)
        address = house.address
        building = house.buldings.first()
        data = {"address": house.address, "bbr": building}
        fields = []
        for field in building._meta.fields:
            name = field.verbose_name
            value = getattr(building, field.name)
            if field.name in BBR.integer_fields:
                fields.append((name, value))
            elif field.name in BBR.categorical_fields:
                [(_, value)] = list(filter(lambda x: x[0] == value, field.choices))
                fields.append((name, value))
        fields.sort(key=lambda x: x[0])
        data["bbr"] = fields

        return render(request, "data_models/adressInfo.html", data)
