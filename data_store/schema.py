import graphene

import data_models.schema


class Query(data_models.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
