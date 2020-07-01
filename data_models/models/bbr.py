from django.db import models
from numpy import array, unique

from data_models.api_wrappers import dawa_id_to_bbr


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
