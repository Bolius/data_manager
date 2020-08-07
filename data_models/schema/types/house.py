import graphene

from .bbr_info import BBRInfo
from data_models.models import House as HOUSE_DB


class House(graphene.ObjectType):
    addressInput = graphene.String(required=False)
    kvhxInput = graphene.String(required=False)
    # water_risk = graphene.NonNull(WaterRisk)
    bbr_info = graphene.NonNull(BBRInfo)

    def resolve_bbr_info(parent, info):
        if parent.addressInput is not None:
            return HOUSE_DB.add_house(address_text=parent.addressInput).buldings.first()
        elif parent.kvhxInput is not None:
            return HOUSE_DB.add_house(kvhx=parent.kvhxInput).buldings.first()

    #
    # def resolve_water_risk(parent, info):
    #     bbr_info = parent.resolve_bbr_info(info)
    #     return WaterRisk(address=bbr_info.address, id=bbr_info.bbr_id)
