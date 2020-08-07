from data_models.models import BBR
from graphene_django.types import DjangoObjectType


class BBRInfo(DjangoObjectType):
    class Meta:
        name = "BBRInfo"
        description = "Data om boligen fra Bygnings- og Boligregistret (BBR)"
        model = BBR

    # bbr_id = graphene.String(description="bbr id", required=True)
    # size = graphene.Int(description="Boligstørrelse i kvadratmeter", required=True)
    # ground_size = graphene.Int(
    #     description="Grundstørrelse i kvadratmeter", required=True
    # )
    # type = graphene.String(description="Anvendelse", required=True)
    # address = graphene.String(description="Adresselinje", required=True)
    # kvhx = graphene.String(description="KVHX i dawa format", required=True)
    # build_year = graphene.Int(description="Bygningsår", required=True)
    # rebuild_year = graphene.Int(description="Renoveringsår", required=True)
    # nr_floors = graphene.Int(description="Antal etager", required=True)
    # prop_type = graphene.String(description="Boligtype", required=True)
    # has_basement = graphene.Boolean(description="Har den kælder?", required=True)
    # basement_area = graphene.Int(description="Kælderareal", required=True)
    # wall_material = graphene.String(
    #     description="Husets Ydervægsmateriale", required=True
    # )
    # roof_area = graphene.Int(description="Samlet tagareal", required=True)
    # nrg_heat = graphene.String(description="Opvarmningsform", required=True)
    # lat = graphene.Float(description="Breddegrad", required=True)
    # long = graphene.Float(description="Længdegrad", required=True)
    # x = graphene.Float(description="utm_x", required=True)
    # y = graphene.Float(description="utm_y", required=True)
