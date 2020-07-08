from __future__ import unicode_literals

from django.contrib.gis.db import models
import geojson
from django.core.serializers import serialize
import data_models.models as data_models


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
        }
        municipalities = Municipality.objects.all()

        for municipality in municipalities:
            res["data"].append(
                {
                    "admin_code": municipality.admin_code,
                    "name": municipality.name,
                    "nr_houses": data_models.House.objects.filter(
                        municipality=municipality
                    ).count(),
                }
            )
        return res

    # TODO look at these fields?
    # nr_houses = models.IntegerField("Antal huse")
    # basements = models.FloatField("Antal huse med kælder")
    # avg_size = models.FloatField("Gnst størrelse")
    # avg_nr_rooms = models.FloatField("Gnst antal værelser")
    # avg_build_year = models.IntegerField("Gnst byggeår", null=True)
    # subscript_email = models.IntegerField("Tilmeldt - email", null=True)
    # subscript_garden = models.IntegerField("Tilmeldt - have", null=True)
    # subscript_save_energy = models.IntegerField("Tilmeldt - sparenergi", null=True)
    # subscript_climate = models.IntegerField("Tilmeldt - indeklima", null=True)
    # subscript_competition = models.IntegerField("Tilmeldt - konkurrencer", null=True)
    # subscript_cleaning = models.IntegerField("Tilmeldt - rengøring", null=True)
