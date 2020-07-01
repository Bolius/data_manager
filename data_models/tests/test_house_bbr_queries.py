from graphene_django.utils.testing import GraphQLTestCase

from data_models.schema import schema

# import json


class HouseBBRQuriesTest(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_address_bbr(self):
        return None
        # response = self.query(
        #     """{
        #     house(addressInput: "Kjærmarken 103, 6771 Gredstedbro") {
        #         bbrInfo{
        #             size
        #             type
        #             buildYear
        #             nrFloors
        #             propType
        #             hasBasement
        #             x
        #             y
        #         }
        #     }
        #     }"""
        # )
        # self.assertResponseNoErrors(response)
        # bbr = json.loads(response.content)["data"]["house"]["bbrInfo"]
        # self.assertEqual(bbr["size"], 173)
        # self.assertEqual(bbr["hasBasement"], False)

    def test_kvhx_input(self):
        return None
        # response = self.query(
        #     """{
        #     house(kvhxInput: "06157266__10_______"){
        #         bbrInfo{
        #             size
        #             type
        #             buildYear
        #             nrFloors
        #             propType
        #             hasBasement
        #             x
        #             y
        #         }
        #     }
        # }"""
        # )
        # bbr = json.loads(response.content)["data"]["house"]["bbrInfo"]
        # self.assertResponseNoErrors(response)
        # self.assertEqual(bbr["size"], 131)
        # self.assertEqual(bbr["hasBasement"], False)
