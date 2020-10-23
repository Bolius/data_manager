import graphene
from data_models.models import House as HOUSE_DB
from .house import House
from .bbr_info import BBRInfo  # noqa must be loaded for graphene to notice.


class Address(graphene.ObjectType):
    class Meta:
        name = "Address"
        description = "Data om boligen fra Bygnings- og Boligregistret (BBR)"

    house = graphene.Field(House)
    dawa_id_input = graphene.String()

    def resolve_house(parent, info):

        return HOUSE_DB.add_house(access_id=parent.dawa_id_input)
