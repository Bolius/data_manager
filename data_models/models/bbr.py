from django.db import models
from django.db.models import Avg, Count
from numpy import array, unique

from data_models.api_wrappers import dawa_id_to_bbr

from .categoricalMapper import (
    ENERGY_SUPPLY_CHOICES,
    RECIDENTIAL_TYPE_CHOICES,
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

integer_fields = [  # TODO remove this
    "building_area",
    "ground_area",
    "garage_area",
    "carport_area",
    "outhouse_area",
    "roof_area",
    "commercial_area",
    "other_area",
]

categorical_fields = [  # TODO remove this
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
        null=True,
    )
    heat_type = models.CharField(
        "Primært Opvarmningsmiddel",
        max_length=2,
        choices=HEAT_TYPE_CHOICES,
        null=True,
        default="0",
    )

    heat_supply = models.CharField(
        "Supplerende Varmekilde",
        max_length=2,
        choices=HEAT_SUPPLY_INSTALL_CHOICES,
        null=True,
    )
    water_supply = models.CharField(
        "Vandforsyning", max_length=2, choices=WATER_SUPPLY_CHOICES, null=True,
    )
    wall_material = models.CharField(
        "Ydervægs Materiale", max_length=2, choices=WALL_MATERIAL_CHOICES, null=True,
    )

    roofing_material = models.CharField(
        "Tagdækningsmateriale",
        max_length=2,
        choices=ROOFING_MATERIAL_CHOICES,
        null=True,
    )

    property_type = models.CharField(
        "Boligtype", max_length=2, choices=PROPERTY_TYPE_CHOICES, null=True,
    )

    kitchen_facility = models.CharField(
        "køkkenforhold", max_length=2, choices=KITCHEN_FACILITY, null=True,
    )

    toilet_facility = models.CharField(
        "Toiletforhold", max_length=2, choices=TOILET_FACILITY, null=True,
    )

    bathing_facility = models.CharField(
        "badeforhold", max_length=2, choices=BATHING_FACILITY, null=True
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
        building.residential_type = data["ENH_ANVEND_KODE"]
        building.heat_install = data["bygning"]["VARMEINSTAL_KODE"]
        building.heat_type = (
            "0" if (val := data["bygning"]["OPVARMNING_KODE"]) is None else val
        )
        building.heat_supply = "0" if (val := data["VARME_SUPPL_KODE"]) is None else val
        building.water_supply = data["bygning"]["BYG_VANDFORSY_KODE"]
        building.wall_material = data["bygning"]["YDERVAEG_KODE"]
        building.roofing_material = data["bygning"]["TAG_KODE"]
        building.property_type = data["BOLIGTYPE_KODE"]
        building.kitchen_facility = data["KOEKKEN_KODE"]
        building.toilet_facility = data["TOILET_KODE"]
        building.bathing_facility = data["BAD_KODE"]
        building.save()

    @staticmethod
    def accumulated_sum_for_catatgorical(field, min_year, max_year):
        year_value = list(
            BBR.objects.values(field, "construction_year").order_by("construction_year")
        )
        result = []
        year = min_year
        keys = [val for (val, _name) in BBR._meta.get_field(field).choices]
        current_result = {key: 0 for key in keys}
        while len(year_value) > 0 and year <= max_year:
            if year != year_value[0]["construction_year"]:
                result.append(current_result.copy())
                year += 1
            else:
                value = year_value.pop(0)
                if value[field] is not None:
                    current_result[value[field]] += 1

        result.append(current_result)
        return result

    @staticmethod
    def get_time_data():
        build_years = BBR.objects.values("construction_year").order_by(
            "construction_year"
        )
        if len(build_years) == 0:
            min_year = 0
            max_year = 0
        else:
            min_year = build_years.first()["construction_year"]
            max_year = build_years.last()["construction_year"]

        build_counts = {}
        for year in build_years.annotate(count=Count("construction_year")):
            build_counts[year["construction_year"]] = year["count"]

        recon_years = {}
        for year in BBR.objects.values("reconstruction_year").annotate(
            count=Count("reconstruction_year")
        ):
            recon_years[year["reconstruction_year"]] = year["count"]

        time_range = list(range(min_year, max_year + 1))
        build_cum_summed = []
        recon_cum_summed = []
        build_total = 0
        recon_total = 0
        for year in time_range:
            build_count = 0 if year not in build_counts.keys() else build_counts[year]
            build_total += build_count
            build_cum_summed.append(build_total)

            recon_count = 0 if year not in recon_years.keys() else recon_years[year]
            recon_total += recon_count
            recon_cum_summed.append(recon_total)

        return {
            "time_range": time_range,
            "houses_per_year": build_cum_summed,
            "recon_per_year": recon_cum_summed,
            "categorical": {
                "heat_install": BBR.accumulated_sum_for_catatgorical(
                    "heat_install", min_year, max_year
                )
            },
        }

    @staticmethod
    def _compute_rolling_avgs(field, min_year, max_year):
        year_avgs = (
            BBR.objects.filter(**{field + "__gte": "0"})
            .values("construction_year")
            .annotate(Avg(field))
            .order_by("construction_year")
        )
        yearly_averages = {}
        for yearly_avg in year_avgs:
            yearly_averages[yearly_avg["construction_year"]] = yearly_avg[
                field + "__avg"
            ]

        averages = []
        nr_year_rolls = 5
        for year in range(min_year, max_year + 1):
            lower_limit = ans if (ans := year - nr_year_rolls) >= min_year else min_year
            upper_limit = ans if (ans := year + nr_year_rolls) <= max_year else max_year
            to_roll = []
            for other_year in range(lower_limit, upper_limit + 1):
                if other_year in yearly_averages.keys():
                    to_roll.append(yearly_averages[other_year])
            averages.append(sum(to_roll) / (ans if (ans := len(to_roll)) > 0 else 1))

        return _fill_zeroes(averages)

    @staticmethod
    def get_rolling_avgs():
        build_years = BBR.objects.values("construction_year").order_by(
            "construction_year"
        )  # TODO pass as variable
        if len(build_years) == 0:
            min_year = 0
            max_year = 0
        else:
            min_year = build_years.first()["construction_year"]
            max_year = build_years.last()["construction_year"]

        return {
            "time_range": list(range(min_year, max_year + 1)),
            "bulding_area": BBR._compute_rolling_avgs(
                "building_area", min_year, max_year
            ),
            "ground_area": BBR._compute_rolling_avgs("ground_area", min_year, max_year),
            "roof_area": BBR._compute_rolling_avgs("roof_area", min_year, max_year),
            "num_toilets": BBR._compute_rolling_avgs("num_toilets", min_year, max_year),
            "num_rooms": BBR._compute_rolling_avgs("num_rooms", min_year, max_year),
            "num_floors": BBR._compute_rolling_avgs("num_floors", min_year, max_year),
            "garage_area": BBR._compute_rolling_avgs("garage_area", min_year, max_year),
            "outhouse_area": BBR._compute_rolling_avgs(
                "outhouse_area", min_year, max_year
            ),
        }

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


def _fill_zeroes(data):
    lower_val = 0
    for i in range(len(data)):
        lower_val = data[i] if data[i] > 0 else lower_val
        if data[i] == 0:
            upper_value = 0
            for j in range(i + 1, len(data)):
                if data[j] > 0:
                    upper_value = data[j]
                    break
            upper_value = upper_value if upper_value > 0 else lower_val
            data[i] = (upper_value + lower_val) / 2
    return data
