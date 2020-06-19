""" A model of the municipality data """
from __future__ import unicode_literals

from django.contrib.gis.db import models

from .geography import City


class NewsletterType(models.Model):
    newsletter_name = models.CharField("Nyhedsbrevstype", max_length=200)
    active = models.BooleanField()


class Subscription(models.Model):
    zip_code = models.IntegerField("Postnummer")
    active = models.BooleanField()

    city = models.ForeignKey(City, on_delete=models.CASCADE)
    newletter = models.ForeignKey(NewsletterType, on_delete=models.CASCADE)
