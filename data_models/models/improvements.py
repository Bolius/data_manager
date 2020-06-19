""" A model of the improvement suggestions from energy rapports """
from __future__ import unicode_literals

from django.db import models

from . import House


class Improvement(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, primary_key=False)
    seeb = models.CharField("SEEB klasse", max_length=7)
    co2Save = models.FloatField("CO2 Saved", blank=True, null=True)
    fuelSave = models.FloatField("Fuel Saved", blank=True, null=True)
    fuelMaterial = models.CharField(
        "Fuel material", blank=True, null=True, max_length=50
    )
    fuelUnit = models.CharField("Fuel Unit", blank=True, null=True, max_length=50)
    moneySave = models.IntegerField("Money Saved", blank=True, null=True)
    long_text = models.TextField("Lang beskrivelse")
    short_text = models.CharField("Kort beskrivelse", max_length=700)
    profitable = models.CharField("Profitabel beskrivelse", max_length=50)


allSeebs = [
    "1-1-1-0",
    "1-3-1-0",
    "4-1-3-0",
    "1-3-3-0",
    "1-2-1-0",
    "2-1-5-0",
    "3-1-3-0",
    "2-2-2-0",
    "2-2-3-0",
    "1-4-1-0",
    "2-1-6-0",
    "2-2-4-0",
    "1-2-2-0",
    "1-4-2-0",
    "1-2-3-0",
    "2-1-2-0",
    "1-2-4-0",
    "1-4-3-0",
    "1-1-2-0",
    "3-1-5-0",
    "2-1-1-0",
    "1-4-4-0",
    "1-2-2-1",
    "1-3-2-0",
    "3-1-1-0",
    "3-1-4-0",
    "2-1-3-0",
    "1-5-1-0",
    "1-4-1-1",
    "2-1-4-0",
    "2-2-1-0",
    "1-2-3-1",
    "1-5-2-0",
    "1-4-4-1",
    "4-1-4-0",
    "1-2-1-1",
    "4-1-1-0",
    "4-1-2-0",
    "1-4-3-1",
    "1-4-2-1",
    "1-4-5-0",
    "1-1-3-0",
]
