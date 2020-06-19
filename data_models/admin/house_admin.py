""" Specifies which parts of the data models are visible in the admin UI """
from django.contrib import admin

from data_models.models import House
from data_models.models.house import hash_address


class HouseAdmin(admin.ModelAdmin):
    """ Specifies how the house model should appear """

    list_filter = ("energyLabel", "type", "heat_type", "wal_material", "energy_type")
    fieldsets = [
        ("Lokation", {"fields": ("address", "zipCode", "parish")}),
        (
            "House info",
            {
                "fields": (
                    "energyLabel",
                    "type",
                    "ownership",
                    "heat_type",
                    "build_year",
                    "recon_year",
                    "roof_type",
                    "energy_type",
                    "bis_area",
                    "sup_heating",
                )
            },
        ),
        (
            "House size",
            {
                "fields": (
                    "size",
                    "oth_area",
                    "nr_rooms",
                    "nr_baths",
                    "nr_toilets",
                    "total_area",
                    "basement_area",
                    "basement_area_used",
                    "roof_area",
                    "nr_of_floors",
                    "garage_size",
                    "out_room_size",
                    "heat1_type",
                    "heat2_type",
                    "water_supply",
                    "wal_material",
                )
            },
        ),
    ]

    list_display = (
        "kvh",
        "geo_x",
        "geo_y",
        "address",
        "zipCode",
        "size",
        "type",
        "parish",
        "ownership",
        "heat_type",
        "build_year",
        "recon_year",
        "roof_type",
        "energy_type",
        "bis_area",
        "oth_area",
        "nr_rooms",
        "nr_baths",
        "nr_toilets",
        "total_area",
        "sup_heating",
        "basement_area",
        "basement_area_used",
        "roof_area",
        "nr_of_floors",
        "garage_size",
        "out_room_size",
        "heat1_type",
        "heat2_type",
        "water_supply",
        "wal_material",
        "prop_value",
        "ground_value",
        "prop_type",
        "energyLabel",
    )

    def hash_address(self, request, queryset):
        for house in queryset:
            house.address = hash_address(house.address)
            house.save()

    # def check_dublets(self, request, queryset):
    #     for house in queryset:
    #         houses = House.objects.filter(address=house.address)
    #         if len(houses) > 1:
    #             surveys = KomfortSurvey.objects.filter(house__address=houses[0].address)
    #             if len(surveys) > 1:
    #                 for i in range(1, len(surveys)):
    #                     surveys[i].delete()
    #             else:
    #                 for i in range(1, len(houses)):
    #                     houses[i].delete()

    actions = ["hash_address", "check_dublets"]


admin.site.register(House, HouseAdmin)
