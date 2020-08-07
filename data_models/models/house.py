""" A model of the komfort survey data """
from __future__ import unicode_literals

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
