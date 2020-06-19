""" A model of domain fields """
from __future__ import unicode_literals

from django.db import models


class Domain(models.Model):
    name = models.CharField("Navn", max_length=200)
    value = models.CharField("Værdi", max_length=200, null=True)
    type = models.CharField("Type", max_length=200)
    description = models.CharField("Beskrivelse", max_length=400)
    source = models.CharField("Kilde", max_length=200)


class Category(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    name = models.CharField("Navn", max_length=200)
    value = models.CharField("Værdi", max_length=200)
