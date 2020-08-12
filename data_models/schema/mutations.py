import graphene
from data_models.tests.factories import add_houses


class AddHouses(graphene.Mutation):
    class Arguments:
        nr_houses = graphene.Int()

    success = graphene.Boolean()
    houses_added = graphene.Int()

    def mutate(root, info, nr_houses):
        count = len(add_houses(nr_houses))
        success = count >= nr_houses
        return AddHouses(success=success, houses_added=count)


class Mutations(graphene.ObjectType):
    add_houses = AddHouses.Field()
