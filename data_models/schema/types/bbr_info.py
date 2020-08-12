from graphene_django.types import DjangoObjectType

from data_models.models import BBR


class BBRInfo(DjangoObjectType):
    class Meta:
        name = "BBRInfo"
        description = "Data om boligen fra Bygnings- og Boligregistret (BBR)"
        model = BBR
