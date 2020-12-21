""" A model of the komfort survey data """
from __future__ import unicode_literals

import json
import os

import requests
from django.contrib.gis.db import models as geo_models
from django.contrib.gis.geos import Point

from data_models.api_wrappers import (
    access_id_to_address,
    address_to_kvhx,
    kvhx_to_address,
)

from .bbr import BBR
from .municipalities import Municipality


class House(geo_models.Model):  # TODO rename house address
    dawa_id = geo_models.CharField("DAWA_ID", unique=True, max_length=40)
    access_id = geo_models.CharField(
        "Adgangs adresse id", max_length=40
    )  # TODO should be uniqe?
    zip_code = geo_models.IntegerField("Postnummer")
    address = geo_models.CharField("Adresse", unique=True, max_length=200)
    kvhx = geo_models.CharField("Kvhx", unique=True, max_length=200)
    coordinates = geo_models.PointField("Lokation")
    municipality = geo_models.ForeignKey(
        "Municipality", on_delete=geo_models.CASCADE, related_name="addresses"
    )

    def __str__(self):
        return f"Adgangsadresse: {self.access_id}"

    @staticmethod
    def add_house(access_id=None, kvhx=None, address_text=None):
        if (access_id, kvhx, address_text) == (None, None, None):
            raise ValueError("Either access_id, address text or kvhx must be specified")
        if access_id is not None:
            houses = House.objects.filter(access_id=access_id)
            if len(houses) > 0:
                return houses[0]

        if kvhx is not None or address_text is not None:
            kvhx = address_to_kvhx(address_text) if kvhx is None else kvhx
            houses = House.objects.filter(kvhx=kvhx)
            if len(houses) > 0:
                return houses[0]
            data = kvhx_to_address(kvhx)
        else:
            houses = House.objects.filter(access_id=access_id)
            if len(houses) > 0:
                return houses[0]
            data = access_id_to_address(access_id)
        if len(houses := House.objects.filter(address=data["adressebetegnelse"])) > 0:
            return houses[0]
        house = House()
        house.dawa_id = data["id"]
        house.access_id = data["adgangsadresse"]["id"]
        house.zip_code = int(data["adgangsadresse"]["postnummer"]["nr"])
        house.address = data["adressebetegnelse"]
        house.kvhx = data["kvhx"]
        house.municipality = Municipality.objects.get(
            admin_code=data["adgangsadresse"]["kommune"]["kode"]
        )
        lat, lon = data["adgangsadresse"]["adgangspunkt"]["koordinater"]
        house.coordinates = Point(lat, lon, srid=4326)
        house.save()
        BBR.add_buldings(house)
        return house

    @staticmethod
    def add_bbr(bbrID):
        url = f"https://apps.conzoom.eu/api/v1/values/dk/unit/{bbrID}"
        header = {"authorization": f'Basic {os.environ["API_KEY"]}'}
        response = requests.request("GET", url, headers=header)
        if response.status_code != 200:
            raise ValueError("Non '200' return code from bbr")
        data = json.loads(response.content)

        house = House()
        house.dawa_id = data["values"]["acadr_bbrid"]
        house.access_id = data["values"]["acadr_bbrid"]
        house.zip_code = int(data["values"]["pcode"])
        house.address = data["values"]["acadr_name"]
        house.kvhx = data["values"]["kvhx_dawa"]
        house.municipality = Municipality.objects.get(
            admin_code="0" + data["values"]["muni"]
        )
        lat, lon = data["values"]["acadr_loc"]["x"], data["values"]["acadr_loc"]["y"]
        house.coordinates = Point(lat, lon, srid=4326)
        if House.objects.filter(access_id=house.access_id).count() < 1:
            house.save()
        bulding = BBR(accsses_address=house)
        bulding.construction_year = int(data["values"]["bld_conyear"].split("-")[0])
        if data["values"]["bld_reconyear"] is not None:
            bulding.reconstruction_year = int(
                data["values"]["bld_reconyear"].split("-")[0]
            )
        bulding.building_area = data["values"]["bld_area_resi"]
        bulding.ground_area = data["values"]["bld_area_total"]
        bulding.garage_area = data["values"]["bld_area_garage"]
        bulding.carport_area = data["values"]["bld_area_carport"]
        bulding.roof_area = (
            0
            if data["values"]["bld_area_roof"] is None
            else data["values"]["bld_area_roof"]
        )
        bulding.commercial_area = data["values"]["bld_area_com"]
        bulding.other_area = data["values"]["bld_area_other"]
        if data["values"]["bld_area_basement"] is not None:
            bulding.basement_area = data["values"]["bld_area_basement"]

        bulding.num_floors = data["values"]["bld_floors"]
        bulding.num_baths = data["values"]["unit_rooms_bath"]
        bulding.num_toilets = data["values"]["unit_rooms_toilet"]
        bulding.num_rooms = data["values"]["unit_rooms"]
        bulding.residential_type = data["values"]["unit_usage"]
        bulding.energy_type = "0"
        bulding.heat_install = "0"
        bulding.heat_type = "0"
        bulding.heat_supply = "0"
        bulding.water_supply = "0"
        bulding.wall_material = "0"
        bulding.roofing_material = "0"
        bulding.property_type = "0"
        bulding.kitchen_facility = "0"
        bulding.toilet_facility = "0"
        bulding.bathing_facility = "0"
        return bulding, house


houseFields = [
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
