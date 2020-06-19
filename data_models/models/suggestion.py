""" A model of the komfort survey data """
from __future__ import unicode_literals

from django.db import models

seebs = [
    "1-1-1-0",
    "1-1-2-0",
    "1-2-1-0",
    "1-2-2-0",
    "1-2-3-0",
    "1-3-1-0",
    "1-3-2-0",
    "1-3-3-0",
    "1-4-1-0",
    "1-4-1-1",
    "1-4-2-0",
    "1-4-3-0",
    "1-4-4-0",
    "1-5-1-0",
    "2-1-1-0",
    "2-1-2-0",
    "2-1-3-0",
    "2-1-4-0",
    "2-1-5-0",
    "2-1-6-0",
    "2-2-1-0",
    "2-2-2-0",
    "2-2-3-0",
    "2-2-4-0",
    "3-1-1-0",
    "3-1-3-0",
    "3-1-4-0",
    "3-1-5-0",
    "4-1-3-0",
]


class Suggestion(models.Model):
    komfort_value = models.CharField(
        "Komfort værdi",
        max_length=200,
        choices=(
            ("1", "Størst"),
            ("2", "Stor"),
            ("3", "Mellem"),
            ("4", "lille"),
            ("5", "mindst"),
        ),
    )
    category = models.CharField(
        "Kategori",
        max_length=200,
        choices=(
            ("install", "Installation"),
            ("clima", "Klimaskærm"),
            ("oth", "Andet"),
        ),
    )
    can_be_suggested = models.BooleanField("Kan blive forslået", default=True)
    internal_note = models.TextField("Interne noter", blank=True, null=True)
    SEEB = models.CharField(
        "SEEB", max_length=8, choices=tuple([(seeb, seeb) for seeb in seebs])
    )

    draft = models.BooleanField("Træk", default=False)
    temperature = models.BooleanField("Temperatur", default=False)
    moisture = models.BooleanField("Fugt", default=False)
    noise = models.BooleanField("Støj", default=False)
    light = models.BooleanField("Dagslys", default=False)
    title = models.CharField("Title", max_length=400)
    description = models.TextField("Beskrivelse", blank=True, null=True)
    read_more = models.URLField(
        "Læs mere link 1:", max_length=400, blank=True, null=True
    )

    read_more1 = models.URLField(
        "Læs mere link 2:", max_length=400, blank=True, null=True
    )

    def to_dict(self):
        return {
            "SEEB": self.SEEB,
            "draft": self.draft,
            "temperature": self.temperature,
            "moisture": self.moisture,
            "noise": self.noise,
            "light": self.light,
            "title": self.title,
            "description": self.description,
            "read_more": self.read_more,
            "read_more1": self.read_more1,
            "category": self.category,
            "komfort_value": self.komfort_value,
        }

    def __str__(self):
        return self.SEEB + ": " + self.title
