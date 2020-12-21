import graphene

from data_models.models import House as HOUSE_DB

from .bbr_info import BBRInfo
from .radon import RadonResp, bbrToRadon


class House(graphene.ObjectType):
    addressInput = graphene.String(required=False)
    bbrID = graphene.String(required=False)
    # water_risk = graphene.NonNull(WaterRisk)
    bbr_info = graphene.NonNull(BBRInfo)
    radon = graphene.Field(RadonResp)

    def resolve_bbr_info(parent, info):
        if parent.addressInput is not None:
            return HOUSE_DB.add_house(address_text=parent.addressInput).buldings.first()
        elif parent.bbrID is not None:
            return HOUSE_DB.add_bbr(parent.bbrID)[0]

    def resolve_radon(parent, info):
        return bbrToRadon(HOUSE_DB.add_bbr(parent.bbrID))

    #
    # def resolve_water_risk(parent, info):
    #     bbr_info = parent.resolve_bbr_info(info)
    #     return WaterRisk(address=bbr_info.address, id=bbr_info.bbr_id)
