# from graphene_django.utils.testing import GraphQLTestCase
# from data_models.schema import schema
# import json
#
#
# class HouseWaterQuriesTest(GraphQLTestCase):
#     GRAPHQL_SCHEMA = schema
#
#     def test_address_hollwing(self):
#         response = self.query(
#             """{
#                 house(addressInput: "Kjærmarken 103, 6771 Gredstedbro") {
#                     waterRisk {
#                         hollowing {
#                             housePercentage
#                             image
#                             areaPercentage
#                         }
#                     }
#                 }
#             }"""
#         )
#         self.assertResponseNoErrors(response)
#         risk = json.loads(response.content)["data"]["house"]["waterRisk"]["hollowing"]
#         self.assertEqual(risk["housePercentage"], 0)
#         self.assertEqual(risk["areaPercentage"], 11)
#
#     def test_address_fastning(self):
#         response = self.query(
#             """{
#                 house(addressInput: "Kjærmarken 103, 6771 Gredstedbro") {
#                     waterRisk {
#                         fastningDegree {
#                             housePercentage
#                             image
#                             areaPercentage
#                         }
#                     }
#                 }
#             }"""
#         )
#         self.assertResponseNoErrors(response)
#         risk = json.loads(response.content)["data"]["house"]["waterRisk"][
#             "fastningDegree"
#         ]
#         self.assertEqual(risk["housePercentage"], 47)
#         self.assertEqual(risk["areaPercentage"], 49)
