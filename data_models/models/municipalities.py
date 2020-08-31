from __future__ import unicode_literals

from django.contrib.gis.db import models


class Municipality(models.Model):
    class Meta:
        verbose_name_plural = "Kommuner"
        verbose_name = "Kommune"
        ordering = ["name"]

    name = models.CharField("Kommunenavn", unique=True, max_length=100)
    admin_code = models.CharField("Kommunekode", unique=True, max_length=5)
    geo_boundary = models.MultiPolygonField(srid=4326, verbose_name="Koordinater")
