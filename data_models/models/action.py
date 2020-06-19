""" A model of the komfort survey data """
from __future__ import unicode_literals

from django.db import models

from .session import Session
from .suggestion import Suggestion


class Action(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    proposal = models.ForeignKey(Suggestion, on_delete=models.CASCADE)
    decision = models.CharField(
        "Beslutning",
        max_length=20,
        choices=(
            ("done", "har gjort"),
            ("will", "Vil gøre"),
            ("Not", "vil ikke"),
            ("None", "Ingen beslutning"),
        ),
    )
    propability = models.FloatField("Sandsynlighed")

    def __str__(self):
        return "Session: " + str(self.proposal.title)
