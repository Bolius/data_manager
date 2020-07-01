""" A model of the komfort survey data """
from __future__ import unicode_literals

import hashlib
import os

from django.contrib.gis.db import models as geo_models
from django.contrib.gis.geos import Point
from django.db import models

from data_models.api_wrappers import access_id_to_address, kvhx_to_address

from .bbr import BBR
from .city import City

from .categoricalMapper import (  # sup_heat_types,; heat_instal,; water_types,; wall_types,
    ENERGY_TYPE_CHOICES,
    HEAT_TYPE_CHOICES,
    RECIDENTIAL_TYPE_CHOICES,
    ROOF_MATERIAL_CHOICES,
    WALL_MATERIAL_CHOICES,
    WATER_SUPPLY_CHOICES,
)


class CategoricalBBR(models.Model):
    # Material and installations
    residential_type = models.CharField(
        "Boligtype", choices=RECIDENTIAL_TYPE_CHOICES, max_length=200
    )
    heat_type = models.CharField(
        "Opvarmningsform", choices=HEAT_TYPE_CHOICES, max_length=200
    )
    energy_type = models.CharField(
        "Energiforsyning", choices=ENERGY_TYPE_CHOICES, max_length=200
    )
    roof_material = models.CharField(
        "Tagmateriale", choices=ROOF_MATERIAL_CHOICES, max_length=200
    )
    wall_material = models.CharField(
        "Ydervægsmateriale", choices=WALL_MATERIAL_CHOICES, max_length=200
    )
    water_supply = models.CharField(
        "Vandforsyning", choices=WATER_SUPPLY_CHOICES, max_length=200
    )


class House(geo_models.Model):  # TODO rename house address
    dawa_id = geo_models.CharField("DAWA_ID", unique=True, max_length=40)
    access_id = geo_models.CharField(
        "Adgangs adresse id", max_length=40
    )  # TODO should be uniqe?
    zip_code = geo_models.IntegerField("Postnummer")
    address = geo_models.CharField("Adresse", unique=True, max_length=200)
    kvhx = geo_models.CharField("Kvhx", unique=True, max_length=200)
    coordinates = geo_models.PointField("Lokation")
    # cities = geo_models.ManyToManyField(City % TODO do we need this?
    # bbr = geo_models.OneToOneField(BBR, on_delete=models.PROTECT)

    def __str__(self):
        return f"Adgangsadresse: {self.access_id}"

    @staticmethod
    def add_house_by_kvhx(kvhx):
        houses = House.objects.filter(kvhx=kvhx)
        if len(houses) > 0:
            return houses[0]
        data = kvhx_to_address(kvhx)
        house = House()
        house.dawa_id = data["id"]
        house.access_id = data["adgangsadresse"]["id"]
        house.zip_code = int(data["adgangsadresse"]["postnummer"]["nr"])
        house.address = data["adressebetegnelse"]
        house.kvhx = data["kvhx"]
        lat, lon = data["adgangsadresse"]["adgangspunkt"]["koordinater"]
        house.coordinates = Point(lat, lon, srid=4326)
        house.save()
        BBR.add_buldings(house)
        return house

    def add_house_by_access_id(access_id):
        houses = House.objects.filter(access_id=access_id)
        if len(houses) > 0:
            return houses[0]
        data = access_id_to_address(access_id)
        house = House()
        house.dawa_id = data["id"]
        house.access_id = data["adgangsadresse"]["id"]
        house.zip_code = int(data["adgangsadresse"]["postnummer"]["nr"])
        house.address = data["adressebetegnelse"]
        house.kvhx = data["kvhx"]
        lat, lon = data["adgangsadresse"]["adgangspunkt"]["koordinater"]
        house.coordinates = Point(lat, lon, srid=4326)
        house.save()
        BBR.add_buldings(house)
        return house


class NumericBBR(models.Model):
    # Area sizes
    building_area = models.IntegerField("Bygning areal")
    ground_area = models.IntegerField("Grund areal")
    garage_area = models.IntegerField("Garage areal")
    carport_area = models.IntegerField("Carport areal")
    outhouse_area = models.IntegerField("Udestue areal")
    roof_area = models.IntegerField("Loft areal")
    basement_area = models.IntegerField("Kælder areal")
    commercial_area = models.IntegerField("Erhvervs areal")

    # Units
    num_baths = models.IntegerField("Antal badeværelser")
    num_toilets = models.IntegerField("Antal toiletter")
    num_rooms = models.IntegerField("Antal værelser")
    num_floors = models.IntegerField("Antal etager")


def add_bbr(data):
    num_bbr = NumericBBR(
        building_area=data["unit_area_resi"],
        ground_area=data["unit_area_total"],
        garage_area=data["bld_area_garage"],
        carport_area=data["bld_area_carport"],
        outhouse_area=data["bld_area_outhouse"],
        roof_area=data["bld_area_roof"],
        basement_area=data["bld_area_basement"],
        commercial_area=data["bld_area_com"],
        num_baths=data["unit_rooms_bath"],
        num_toilets=data["unit_rooms_toilet"],
        num_rooms=data["unit_rooms"],
        num_floors=data["bld_floors"],
    )

    cat_bbr = CategoricalBBR(
        residential_type=data["unit_resityp_geo"],
        heat_type=data["bld_nrg_heat_instal"],
        energy_type=data["unit_nrg_sup"],
        roof_material=data["bld_roof_material"],
        wall_material=data["bld_wallmatrl"],
        water_supply=data["bld_watersupl"],
    )

    num_bbr.save()
    cat_bbr.save()

    bbr = BBR(
        address=data["unadr_name"],
        zip_code=data["pcode"],
        kvhx=data["kvhx"],
        construction_year=int(data["bld_conyear"][:4]),
        reconstruction_year=int(data["bld_reconyear"][:4]),
        bbr_numeric=num_bbr,
        bbr_categorical=cat_bbr,
    )
    return bbr


def add_house(data):
    zip_code = data["pcode"]
    address = data["unadr_name"]
    kvhx = data["kvhx"]

    # Add bbr info
    if House.objects.filter(kvhx=kvhx).count() == 0:
        lat_lon = eval(data["acadr_loc"])
        try:
            lat_lon.get("lat")
        except ():
            return

        print("add house")
        bbr = add_bbr(data)
        bbr.save()

        # find cities for
        cities = City.objects.filter(
            zip_code_start__lte=zip_code, zip_code_end__gte=zip_code
        )

        lat_lon = eval(data["acadr_loc"])

        house = House(
            address=address,
            zip_code=zip_code,
            kvhx=kvhx,
            lat=lat_lon.get("lat"),
            lon=lat_lon.get("long"),
            bbr=bbr,
        )

        house.save()

        for c in cities:
            house.cities.add(c)

    # Get city that the house belongs to and add


def hash_address(address):
    salted = address + os.environ["SALT"]
    if " " in address:
        return hashlib.sha224(salted.encode("utf-8")).hexdigest()
    else:
        return address


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
