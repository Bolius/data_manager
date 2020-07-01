from django.db import models
from data_models.api_wrappers import dawa_id_to_bbr
from django.db.models import Count


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
        years = BBR.objects.values("construction_year").order_by("construction_year")
        min_year = years.first()["construction_year"]
        max_year = years.last()["construction_year"]

        counts = {}
        for year in years.annotate(count=Count("construction_year")):
            counts[year["construction_year"]] = year["count"]

        time_range = list(range(min_year, max_year + 1))
        cum_summed = {}
        total = 0
        for year in time_range:
            count = 0 if year not in counts.keys() else counts[year]
            total += count
            cum_summed[year] = total

        return {
            "time_range": time_range,
            "houses_per_year": cum_summed,
        }
