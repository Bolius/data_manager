import graphene
from graphql import GraphQLError

from .types import House


class Query(graphene.ObjectType):
    house = graphene.Field(
        House,
        addressInput=graphene.String(required=False),
        kvhxInput=graphene.String(required=False),
        access_id=graphene.String(required=False),
    )

    def resolve_house(self, info, addressInput=None, kvhxInput=None, access_id=None):
        if addressInput is not None:
            return House(addressInput=addressInput)
        # elif access_id is not None:
        #     return Houseadd_house(kvhxInput=access_id)
        elif kvhxInput is not None:
            return House(kvhxInput=kvhxInput)
        else:
            raise GraphQLError("No address or kvhx specified")
