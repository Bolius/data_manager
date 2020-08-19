from __future__ import unicode_literals

# from sentry_sdk import capture_exception, capture_message
import geojson
import pandas as pd
from django.contrib.gis.db import models
from django.core.serializers import serialize
from django.db.models import Avg, Count

from data_models import models as data_models

from .bbr import BBR


class Municipality(models.Model):
    class Meta:
        verbose_name_plural = "Kommuner"
        verbose_name = "Kommune"
        ordering = ["name"]

    name = models.CharField("Kommunenavn", unique=True, max_length=100)
    admin_code = models.CharField("Kommunekode", unique=True, max_length=5)
    geo_boundary = models.MultiPolygonField(srid=4326, verbose_name="Koordinater")

    @staticmethod
    def get_stats():
        res = {
            "geo_data": geojson.loads(
                serialize(
                    "geojson",
                    Municipality.objects.all(),
                    geometry_field="geo_boundary",
                    fields=("name", "admin_code"),
                )
            ),
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
                    "nr_houses": data_models.House.objects.filter(
                        municipality=municipality
                    ).count(),
                }
            )
            muni_averages.append(averages)
            res["categorical"][municipality.admin_code] = {}
            for cat_field in BBR.categorical_fields:
                choices = [
                    field.choices
                    for field in BBR._meta.fields
                    if field.name == cat_field
                ][0]
                res["categorical"][municipality.admin_code][cat_field] = {}
                for val, _name in choices:
                    res["categorical"][municipality.admin_code][cat_field][val] = 0

                counts = buldings_in_muni.values(cat_field).annotate(
                    count=Count(cat_field)
                )
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
