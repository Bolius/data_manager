""" A model of the komfort survey data """
from __future__ import unicode_literals

from django.db import models

from . import House


class KomfortSurvey(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, primary_key=False)
    draft = models.IntegerField("Træk")
    temperature = models.IntegerField("Temperatur")
    moisture = models.IntegerField("Fugt")
    noise = models.IntegerField("Støj")
    light = models.IntegerField("Dagslys")
    smell = models.IntegerField("Lugt")
    roof_isolation = models.BooleanField("Tag isolering", default=False)
    ceiling_isolation = models.BooleanField("Loft isolering", default=False)
    floor_isolation = models.BooleanField("Isolering af gulv", default=False)
    socket_isolation = models.BooleanField("Isolering af sokkel", default=False)
    base_room_isolation = models.BooleanField(
        "Isolering mellem kælder og stue", default=False
    )
    base_inside_isolation = models.BooleanField(
        "Isolering af kældervæg indefra", default=False
    )
    base_outside_isolation = models.BooleanField(
        "Isolering af kældervæg udefra", default=False
    )
    cavity_isolation = models.BooleanField("Hulmursisolering", default=False)
    walls_outside = models.BooleanField("Isolering af ydervæg udefra", default=False)
    walls_inside = models.BooleanField("Isolering af ydervæg indefra", default=False)
    windows = models.BooleanField("Nye vinduer", default=False)
    window_panes = models.BooleanField("Nye ruder", default=False)
    doors = models.BooleanField("Nye yderdøre", default=False)
    top_windows = models.BooleanField("Nye ovenlysvinduer", default=False)
    top_domes = models.BooleanField("Nye ovenlyskupler", default=False)
    window_sealing = models.BooleanField("Tætning af vinduer", default=False)
    remote_heat = models.BooleanField("Skift til fjernvarme", default=False)
    nat_gas = models.BooleanField("Skift til naturgas", default=False)
    bio_fuel = models.BooleanField("Skift til biobrændsel", default=False)
    gas_kettle = models.BooleanField("Ny gaskedel", default=False)
    remot_heat_facil = models.BooleanField("Nyt fjernvarmeanlæg", default=False)
    water_con = models.BooleanField("Ny Varmtvandsbeholder", default=False)
    radiator_valves = models.BooleanField("Nye radiatorventiler", default=False)
    circu_pump_new = models.BooleanField("Ny cirkulationspumpe", default=False)
    circu_pump_mod = models.BooleanField("Ændring af cirkulationspumpe", default=False)
    automate_heat = models.BooleanField("Automatik til varmeanlæg", default=False)
    pipe_isolation = models.BooleanField("Isolering af rør", default=False)
    ventilation_heat = models.BooleanField(
        "Ventilationsanlæg med varmegenvinding", default=False
    )
    sun_heat = models.BooleanField("Solvarmeanlæg", default=False)
    sun_cells = models.BooleanField("Solcelleanlæg", default=False)
    comment = models.CharField("Kommentar", max_length=300, default="")
    heat_pump = models.BooleanField("Skift til varmepumpe", default=False)
    percived_energyLabel = models.CharField(
        "Energimærke",
        max_length=1,
        default="0",
        choices=(
            ("0", ""),
            ("1", "A"),
            ("2", "B"),
            ("3", "C"),
            ("4", "D"),
            ("5", "E"),
            ("6", "F"),
            ("7", "G"),
        ),
    )

    def __str__(self):
        return "svar for " + str(self.house)
