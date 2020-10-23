import graphene
from graphene_django.types import DjangoObjectType

from data_models.models import House as HOUSE_DB


class House(DjangoObjectType):
    class Meta:
        name = "House"
        description = "En adresse"
        model = HOUSE_DB
        exclude = ("coordinates",)
