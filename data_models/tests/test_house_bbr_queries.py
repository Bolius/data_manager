from graphene_django.utils.testing import GraphQLTestCase

from data_models.schema import schema


class HouseBBRQuriesTest(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_address_bbr(self):
        response = self.query(
            """{
            house(addressInput: "Kjærmarken 103, 6771 Gredstedbro") {
                bbrInfo{
                    buildingArea
                }
            }
            }"""
        )
        self.assertResponseNoErrors(response)
        bbr = response.json()["data"]["house"]["bbrInfo"]
        self.assertEqual(bbr["buildingArea"], 173)
