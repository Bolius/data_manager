from __future__ import unicode_literals

from django.db import models


class City(models.Model):
    city_name = models.CharField("Bynavn", max_length=200)
    zip_code_start = models.IntegerField("Postnummer start")
    zip_code_end = models.IntegerField("Postnummer slut")
    municipality = models.ForeignKey(
        "Municipality", related_name="city", on_delete=models.PROTECT
    )  # TODO fix this, points all to 1.
