from graphene_django.utils.testing import GraphQLTestCase

from data_models.schema import schema
from data_models.models import House


class AddHouseMutationTest(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_address_bbr(self):
        self.assertEqual(len(House.objects.all()), 0)
        response = self.query(
            """
                mutation {
                    addHouses(nrHouses: 5){
                        success
                        housesAdded
                    }
                }
            """
        )
        self.assertResponseNoErrors(response)
        response = response.json()["data"]["addHouses"]
        self.assertTrue(response["success"])
        self.assertEqual(response["housesAdded"], 5)
        self.assertEqual(len(House.objects.all()), 5)
