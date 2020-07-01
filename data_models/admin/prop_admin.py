""" Specifies which parts of the data models are visible in the admin UI """
import pandas as pd

from data_models.models import House, Improvement
from data_models.models.house import houseFields
from data_models.models.improvements import allSeebs
from django.contrib import admin


class PropAdmin(admin.ModelAdmin):
    list_filter = ("seeb", "profitable", "fuelUnit")

    fieldsets = [
        (
            "Foredring",
            {
                "fields": (
                    "house",
                    "seeb",
                    "co2Save",
                    "fuelSave",
                    "fuelUnit",
                    "fuelMaterial",
                    "moneySave",
                    "short_text",
                    "profitable",
                    "long_text",
                )
            },
        )
    ]
    list_display = (
        "house",
        "seeb",
        "co2Save",
        "fuelSave",
        "moneySave",
        "short_text",
        "profitable",
        "fuelMaterial",
        "fuelUnit",
    )

    def get_prop_data(request, a, b):
        dicts = []
        houses = House.objects.all()
        for house in houses:
            row = {}
            for field in houseFields:
                row[field] = getattr(house, field)
            cur_seeb = [prop.seeb for prop in Improvement.objects.filter(house=house)]
            if len(cur_seeb) < 1:
                continue
            for seeb in allSeebs:
                row[seeb] = seeb in cur_seeb
            dicts.append(row)
        pd.Dataframe(dicts).to_csv("dump.csv", sep="|")

    actions = ["get_prop_data"]


admin.site.register(Improvement, PropAdmin)
