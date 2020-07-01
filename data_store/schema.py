import data_models.schema
import graphene


class Query(data_models.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
