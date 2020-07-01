from django.db import models
from numpy import array, unique

from data_models.api_wrappers import dawa_id_to_bbr

from .categoricalMapper import (
    BATHING_FACILITY,
    HEAT_INSTALL_CHOICES,
    HEAT_SUPPLY_INSTALL_CHOICES,
    HEAT_TYPE_CHOICES,
    KITCHEN_FACILITY,
    PROPERTY_TYPE_CHOICES,
    ROOFING_MATERIAL_CHOICES,
    TOILET_FACILITY,
    WALL_MATERIAL_CHOICES,
    WATER_SUPPLY_CHOICES,
)

integer_fields = [
    "building_area",
    "ground_area",
    "garage_area",
    "carport_area",
    "outhouse_area",
    "roof_area",
    "commercial_area",
    "other_area",
]

categorical_fields = [
    "heat_install",
    "heat_type",
    "heat_supply",
    "water_supply",
    "wall_material",
    "energy_supply",
    "roofing_material",
    "property_type",
    "kitchen_facility",
    "toilet_facility",
    "bathing_facility",
]


class BBR(models.Model):  # TODO Rename to bulding / house
    accsses_address = models.ForeignKey(
        "House", on_delete=models.PROTECT, related_name="buldings"
    )
    construction_year = models.IntegerField("Byggeår")
    reconstruction_year = models.IntegerField("Renoveringsår", null=True, blank=True)
    building_area = models.IntegerField("Bygning areal")
    ground_area = models.IntegerField("Grund areal")
    garage_area = models.IntegerField("Garage areal")
    carport_area = models.IntegerField("Carport areal")
    outhouse_area = models.IntegerField("Udestue areal")
    roof_area = models.IntegerField("Loft areal")
    commercial_area = models.IntegerField("Erhvervs areal")
    other_area = models.IntegerField("Kælder/loftrum osv.")

    num_floors = models.IntegerField("Antal etager")
    num_baths = models.IntegerField("Antal badeværelser")
    num_toilets = models.IntegerField("Antal toiletter")
    num_rooms = models.IntegerField("Antal værelser")

    heat_install = models.CharField(
        max_length=2, choices=HEAT_INSTALL_CHOICES, default="0"
    )
    heat_type = models.CharField(max_length=2, choices=HEAT_TYPE_CHOICES, default="0")

    heat_supply = models.CharField(
        max_length=2, choices=HEAT_SUPPLY_INSTALL_CHOICES, default="0"
    )
    water_supply = models.CharField(
        max_length=2, choices=WATER_SUPPLY_CHOICES, default="0"
    )
    wall_material = models.CharField(
        max_length=2, choices=WALL_MATERIAL_CHOICES, default="0"
    )

    roofing_material = models.CharField(
        max_length=2, choices=ROOFING_MATERIAL_CHOICES, default="0"
    )

    property_type = models.CharField(
        max_length=2, choices=PROPERTY_TYPE_CHOICES, default="0"
    )

    kitchen_facility = models.CharField(
        max_length=2, choices=KITCHEN_FACILITY, default="0"
    )

    toilet_facility = models.CharField(
        max_length=2, choices=TOILET_FACILITY, default="0"
    )

    bathing_facility = models.CharField(
        max_length=2, choices=BATHING_FACILITY, default="0"
    )

    # bbr_numeric = models.OneToOneField(NumericBBR, on_delete=models.CASCADE, null=True)

    @staticmethod
    def add_buldings(house):
        data = dawa_id_to_bbr(house.dawa_id)[0]
        building = BBR()
        building.accsses_address = house
        building.construction_year = data["bygning"]["OPFOERELSE_AAR"]
        building.reconstruction_year = (
            data["bygning"]["OMBYG_AAR"] if data["bygning"]["OMBYG_AAR"] > 0 else None
        )
        # TODO check if zero for many?
        building.ground_area = data["ENH_ARL_SAML"]
        building.building_area = data["BEBO_ARL"]
        building.garage_area = data["bygning"]["GARAGE_INDB_ARL"]
        building.carport_area = data["bygning"]["CARPORT_INDB_ARL"]
        building.outhouse_area = data["bygning"]["UDESTUE_ARL"]
        building.num_floors = data["bygning"]["ETAGER_ANT"]
        building.roof_area = data["LukOverdaekAreal"]
        building.other_area = data["bygning"]["ANDET_ARL"]
        building.num_rooms = data["VAERELSE_ANT"]
        building.num_baths = data["AntBadevaerelser"]
        building.num_toilets = data["AntVandskylToilleter"]
        building.commercial_area = data["ENH_ERHV_ARL"]

        building.heat_install = (
            data["bygning"]["VARMEINSTAL_KODE"]
            if data["bygning"]["VARMEINSTAL_KODE"] is not None
            else "0"
        )
        building.heat_type = (
            data["bygning"]["OPVARMNING_KODE"]
            if data["bygning"]["OPVARMNING_KODE"] is not None
            else "0"
        )
        building.heat_supply = (
            data["bygning"]["VARME_SUPPL_KODE"]
            if data["bygning"]["VARME_SUPPL_KODE"] is not None
            else "0"
        )
        building.water_supply = (
            data["bygning"]["BYG_VANDFORSY_KODE"]
            if data["bygning"]["BYG_VANDFORSY_KODE"]
            else "0"
        )
        building.wall_material = (
            data["bygning"]["YDERVAEG_KODE"]
            if data["bygning"]["YDERVAEG_KODE"] is None
            else "0"
        )

        building.roofing_material = (
            data["bygning"]["TAG_KODE"] if data["bygning"]["TAG_KODE"] is None else "0"
        )

        building.property_type = (
            data["BOLIGTYPE_KODE"] if data["BOLIGTYPE_KODE"] is None else "0"
        )

        building.kitchen_facility = (
            data["KOEKKEN_KODE"] if data["KOEKKEN_KODE"] is None else "0"
        )

        building.toilet_facility = (
            data["TOILET_KODE"] if data["TOILET_KODE"] is None else "0"
        )

        building.bathing_facility = (
            data["BAD_KODE"] if data["BAD_KODE"] is None else "0"
        )

        building.save()

    @staticmethod
    def get_scatter_points(
        xParam, yParam, valFromX, valToX, valFromY, valToY, yearValue
    ):
        # TODO: check security
        _locals = locals()
        query = (
            f"hs = BBR.objects.filter({xParam}__gte={valFromY}, {xParam}__lte={valToY})"
            if yParam == xParam
            else f"hs = BBR.objects.filter({xParam}__gte={valFromY}, {xParam}__lte={valToY}, {yParam}__gte={valFromX}, {yParam}__lte={valToX})"
        )

        exec(
            query, globals(), _locals,
        )

        bbr = _locals.get("hs")

        hs = array(
            bbr.filter(
                construction_year__gte=yearValue[0],
                construction_year__lte=yearValue[0] + 5,
            ).values_list(xParam, yParam)
        )

        info, counts = None, None
        if hs.size != 0:
            info, counts = unique(hs, return_counts=True, axis=0)
        return info, counts
