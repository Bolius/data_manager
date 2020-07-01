from data_models.api_wrappers import dawa_id_to_bbr
from django.db import models
from django.db.models import Avg, Count


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

    def __str__(self):
        return f"BBR oplysninger for {self.accsses_address}"

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
        building.save()

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
                "garage_area", min_year, max_year
            ),
        }


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
