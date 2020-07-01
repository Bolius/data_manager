""" Specifies which parts of the data models are visible in the admin UI """
import csv

from data_models.models import House, KomfortSurvey
from django.contrib import admin
from django.http import HttpResponse


class KomfortSurveyAdmin(admin.ModelAdmin):
    """ Specifies how the komfortSurvey model should appear """

    fieldsets = [
        ("House", {"fields": ("house", "comment", "percived_energyLabel")}),
        (
            "Indeklima",
            {"fields": ("draft", "temperature", "moisture", "noise", "light", "smell")},
        ),
        (
            "Renovering af isolation",
            {
                "fields": (
                    "roof_isolation",
                    "ceiling_isolation",
                    "floor_isolation",
                    "socket_isolation",
                    "base_room_isolation",
                    "base_inside_isolation",
                    "base_outside_isolation",
                    "walls_outside",
                    "walls_inside",
                    "windows",
                    "window_panes",
                    "doors",
                    "top_windows",
                    "top_domes",
                    "window_sealing",
                    "cavity_isolation",
                )
            },
        ),
        (
            "Renovering af varmekilder",
            {
                "fields": (
                    "remote_heat",
                    "nat_gas",
                    "bio_fuel",
                    "gas_kettle",
                    "water_con",
                    "remot_heat_facil",
                    "radiator_valves",
                    "circu_pump_new",
                    "sun_heat",
                    "sun_cells",
                    "heat_pump",
                    "circu_pump_mod",
                    "automate_heat",
                    "pipe_isolation",
                    "ventilation_heat",
                )
            },
        ),
    ]

    list_display = (
        "draft",
        "temperature",
        "moisture",
        "noise",
        "light",
        "smell",
        "doors",
        "comment",
        "roof_isolation",
        "ceiling_isolation",
        "floor_isolation",
        "top_domes",
        "floor_isolation",
        "socket_isolation",
        "base_room_isolation",
        "windows",
        "base_inside_isolation",
        "base_outside_isolation",
        "cavity_isolation",
        "walls_outside",
        "walls_inside",
        "window_panes",
        "top_windows",
        "window_sealing",
        "remote_heat",
        "nat_gas",
        "bio_fuel",
        "gas_kettle",
        "remot_heat_facil",
        "water_con",
        "radiator_valves",
        "circu_pump_new",
        "circu_pump_mod",
        "automate_heat",
        "pipe_isolation",
        "heat_pump",
        "ventilation_heat",
        "sun_heat",
        "sun_cells",
        "percived_energyLabel",
    )
    list_filter = (
        "roof_isolation",
        "ceiling_isolation",
        "floor_isolation",
        "floor_isolation",
        "socket_isolation",
        "base_room_isolation",
        "windows",
        "base_inside_isolation",
        "base_outside_isolation",
        "cavity_isolation",
        "walls_outside",
        "walls_inside",
        "window_panes",
        "top_windows",
        "top_domes",
        "window_sealing",
        "remote_heat",
        "nat_gas",
        "bio_fuel",
        "gas_kettle",
        "remot_heat_facil",
        "water_con",
        "radiator_valves",
        "circu_pump_new",
        "circu_pump_mod",
        "automate_heat",
        "pipe_isolation",
        "heat_pump",
        "ventilation_heat",
        "sun_heat",
        "sun_cells",
        "percived_energyLabel",
    )

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        komfort_fields = [field.name for field in meta.fields]
        house_fields = [field.name for field in House._meta.fields]
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)
        writer.writerow(komfort_fields + house_fields)
        for obj in queryset:
            komfort_row = [getattr(obj, field) for field in komfort_fields]
            house_row = [getattr(obj.house, field) for field in house_fields]
            writer.writerow(komfort_row + house_row)
        return response

    def export_ai_csv(self, request, queryset):
        """ The fields needed for the training set and the targets """
        meta = self.model._meta
        komfort_fields = ["temperature", "draft", "moisture", "noise", "smell", "light"]

        house_fields = [
            "zipCode",
            "size",
            "type",
            "geo_x",
            "geo_y",
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
        ]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)
        writer.writerow(komfort_fields + house_fields)
        for obj in queryset:
            komfort_row = [getattr(obj, field) for field in komfort_fields]
            house_row = [getattr(obj.house, field) for field in house_fields]
            writer.writerow(komfort_row + house_row)
        return response

    export_ai_csv.short_description = "Export AI Training File"
    export_as_csv.short_description = "Create csv file for Excel etc."
    actions = ["export_as_csv", "export_ai_csv"]


admin.site.register(KomfortSurvey, KomfortSurveyAdmin)
