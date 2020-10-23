import graphene
from graphql import GraphQLError

from .types import Address


class Query(graphene.ObjectType):
    address = graphene.Field(Address, dawa_id=graphene.String())

    def resolve_address(self, info, dawa_id):
        if dawa_id is not None:
            return Address(dawa_id_input=dawa_id)
        else:
            raise GraphQLError("No address or kvhx specified")
