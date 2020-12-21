from django.db import models
from numpy import array, unique

from data_models.api_wrappers import dawa_id_to_bbr

from .categoricalMapper import (
    BATHING_FACILITY,
    ENERGY_SUPPLY_CHOICES,
    HEAT_INSTALL_CHOICES,
    HEAT_SUPPLY_INSTALL_CHOICES,
    HEAT_TYPE_CHOICES,
    KITCHEN_FACILITY,
    PROPERTY_TYPE_CHOICES,
    RECIDENTIAL_TYPE_CHOICES,
    ROOFING_MATERIAL_CHOICES,
    TOILET_FACILITY,
    WALL_MATERIAL_CHOICES,
    WATER_SUPPLY_CHOICES,
)


class BBR(models.Model):  # TODO Rename to bulding / house
    integer_fields = [
        "construction_year",
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
        "energy_type",
        "roofing_material",
        "property_type",
        "kitchen_facility",
        "toilet_facility",
        "bathing_facility",
        "residential_type",
    ]

    accsses_address = models.ForeignKey(
        "House", on_delete=models.CASCADE, related_name="buldings"
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
    basement_area = models.IntegerField("Kælder størrelse", default=0)

    num_floors = models.IntegerField("Antal etager")
    num_baths = models.IntegerField("Antal badeværelser")
    num_toilets = models.IntegerField("Antal toiletter")
    num_rooms = models.IntegerField("Antal værelser")
    # TODO set to choicefield
    residential_type = models.CharField(
        "Boligtype", max_length=7, choices=RECIDENTIAL_TYPE_CHOICES
    )

    energy_type = models.CharField(
        "Primær Energiforsyning",
        max_length=2,
        choices=ENERGY_SUPPLY_CHOICES,
        default="0",
    )
    heat_install = models.CharField(
        "Primær varmeinstallation",
        max_length=2,
        choices=HEAT_INSTALL_CHOICES,
        default="0",
    )
    heat_type = models.CharField(
        "Primært Opvarmningsmiddel",
        max_length=2,
        choices=HEAT_TYPE_CHOICES,
        default="0",
    )

    heat_supply = models.CharField(
        "Supplerende Varmekilde",
        max_length=2,
        choices=HEAT_SUPPLY_INSTALL_CHOICES,
        default="0",
    )
    water_supply = models.CharField(
        "Vandforsyning",
        max_length=2,
        choices=WATER_SUPPLY_CHOICES,
        default="0",
    )
    wall_material = models.CharField(
        "Ydervægs Materiale",
        max_length=2,
        choices=WALL_MATERIAL_CHOICES,
        default="0",
    )

    roofing_material = models.CharField(
        "Tagdækningsmateriale",
        max_length=2,
        choices=ROOFING_MATERIAL_CHOICES,
        default="0",
    )

    property_type = models.CharField(
        "Boligtype",
        max_length=2,
        choices=PROPERTY_TYPE_CHOICES,
        default="0",
    )

    kitchen_facility = models.CharField(
        "køkkenforhold", max_length=2, choices=KITCHEN_FACILITY, default="0"
    )

    toilet_facility = models.CharField(
        "Toiletforhold", max_length=2, choices=TOILET_FACILITY, default="0"
    )

    bathing_facility = models.CharField(
        "badeforhold", max_length=2, choices=BATHING_FACILITY, default="0"
    )

    def __str__(self):
        return f"BBR oplysninger for {self.accsses_address}"

    @staticmethod
    def field_to_desc(field_name):
        field_name = field_name.replace("__avg", "")
        return [
            field.verbose_name
            for field in BBR._meta.concrete_fields
            if field.name == field_name
        ][0]

    @staticmethod
    def choice_to_desc(field_name, choice):
        choices = [
            field.choices
            for field in BBR._meta.concrete_fields
            if field.name == field_name
        ][0]
        return [desc for val, desc in choices if val == str(choice)][0]

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

        building.energy_type = "0" if (val := data["ENERGI_KODE"]) is None else val
        building.heat_install = (
            "0" if (val := data["bygning"]["VARMEINSTAL_KODE"]) is None else val
        )
        building.heat_type = (
            "0" if (val := data["bygning"]["OPVARMNING_KODE"]) is None else val
        )
        building.heat_supply = "0" if (val := data["VARME_SUPPL_KODE"]) is None else val

        building.water_supply = data["bygning"]["BYG_VANDFORSY_KODE"]
        if building.water_supply not in [nr for nr, _type in WATER_SUPPLY_CHOICES]:
            building.water_supply = "0"
        building.water_supply = data["bygning"]["BYG_VANDFORSY_KODE"]
        building.wall_material = data["bygning"]["YDERVAEG_KODE"]
        building.roofing_material = data["bygning"]["TAG_KODE"]
        building.property_type = data["BOLIGTYPE_KODE"]
        building.kitchen_facility = (
            "0" if (val := data["KOEKKEN_KODE"]) is None else val
        )
        building.toilet_facility = "0" if (val := data["TOILET_KODE"]) is None else val
        building.bathing_facility = "0" if (val := data["BAD_KODE"]) is None else val
        # TODO should we change this?
        resiType = data["ENH_ANVEND_KODE"]
        if resiType in [nr for nr, _type in RECIDENTIAL_TYPE_CHOICES]:
            building.residential_type = data["ENH_ANVEND_KODE"]
        else:
            building.residential_type = "oth"
        building.save()

    @staticmethod
    def get_scatter_points(  # TODO DELETE THIS
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
            query,
            globals(),
            _locals,
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
