import graphene

from .mutations import Mutations
from .queries import Query

schema = graphene.Schema(query=Query, mutation=Mutations)
