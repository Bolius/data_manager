import graphene


class Radon(graphene.ObjectType):
    class Meta:
        name = "radon"
        description = "Info om radon "

    bqm3 = graphene.Float(required=True, description="Bq/m^3")
    soil_type = graphene.String(required=True, description="Jordbundstype")
