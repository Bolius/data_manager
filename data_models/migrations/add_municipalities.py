# Generated by Django 3.0.5 on 2020-05-29 13:17

import json

from django.contrib.gis.geos import MultiPolygon, Polygon
from django.db import migrations


def load_municipalities(apps, schema_editor):
    Municipality = apps.get_model("data_models", "Municipality")
    with open("public_data/municipalities.geojson") as json_file:
        municipalities = json.load(json_file)["features"]
    parsed_municipalities = {}
    for municipality in municipalities:
        parsed_muni = {
            "admin_code": municipality["properties"]["KOMKODE"],
            "name": municipality["properties"]["KOMNAVN"],
            "boundary": [
                Polygon(
                    [
                        (x, y)
                        for [x, y, _z] in municipality["geometry"]["coordinates"][0]
                    ]
                )
            ],
        }

        if parsed_muni["admin_code"] in parsed_municipalities:
            parsed_municipalities[parsed_muni["admin_code"]]["boundary"].append(
                parsed_muni["boundary"][0]
            )
        else:
            parsed_municipalities[parsed_muni["admin_code"]] = parsed_muni
    for muni_code in parsed_municipalities:
        parsed_muni = parsed_municipalities[muni_code]
        Municipality.objects.create(
            name=parsed_muni["name"],
            admin_code=parsed_muni["admin_code"],
            geo_boundary=MultiPolygon(parsed_muni["boundary"]),
        )


class Migration(migrations.Migration):

    dependencies = [
        ("data_models", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_municipalities),
    ]
