""" A model of the komfort survey data """
from __future__ import unicode_literals

from django.db import models

from .house import House


class Session(models.Model):
    creation = models.DateTimeField("oprettet", auto_now_add=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    original_draft = models.FloatField("Forslået træk")
    updated_draft = models.FloatField("Bruger træk")
    original_temperature = models.FloatField("Forslået temperatur")
    updated_temperature = models.FloatField("Bruger temperatur")
    original_moisture = models.FloatField("Forslået fugt")
    updated_moisture = models.FloatField("Bruger fugt")
    original_light = models.FloatField("Forslået lys")
    updated_light = models.FloatField("Bruger lys")
    original_noise = models.FloatField("Forslået støj")
    updated_noise = models.FloatField("Bruger støj")

    def __str__(self):
        return "Session: " + str(self.creation)
