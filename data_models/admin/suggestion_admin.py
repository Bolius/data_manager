""" Specifies which parts of the data models are visible in the admin UI """
import pandas as pd

from data_models.models import House, Improvement, Suggestion
from data_models.models.house import houseFields
from data_models.models.improvements import allSeebs
from django.contrib import admin


class SuggestionAdmin(admin.ModelAdmin):
    list_filter = (
        "komfort_value",
        "category",
        "can_be_suggested",
        "draft",
        "temperature",
        "moisture",
        "noise",
        "light",
    )
    fieldsets = [
        (
            "Intern information",
            {
                "fields": (
                    "can_be_suggested",
                    "internal_note",
                    "category",
                    "komfort_value",
                )
            },
        ),
        (
            "Extern information",
            {"fields": ("SEEB", "title", "description", "read_more", "read_more1")},
        ),
        (
            "Afhjælper",
            {"fields": ("draft", "temperature", "moisture", "noise", "light")},
        ),
    ]
    list_display = (
        "SEEB",
        "category",
        "title",
        "draft",
        "temperature",
        "moisture",
        "noise",
        "light",
        "description",
        "can_be_suggested",
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


admin.site.register(Suggestion, SuggestionAdmin)
