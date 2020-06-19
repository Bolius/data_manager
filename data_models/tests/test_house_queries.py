# from graphene_django.utils.testing import GraphQLTestCase
# from data_models.schema import schema
# import json
#
#
# class HouseQuriesTest(GraphQLTestCase):
#     GRAPHQL_SCHEMA = schema
#
#     def test_no_input(self):
#         response = self.query(
#             """
#                 {
#                   house {
#                     waterRisk {
#                       hollowing {
#                         image
#                       }
#                     }
#                   }
#                 }
#             """
#         )
#         print(
#             "Expected to see line with 'GraphQLLocatedError: No address or kvhx specified'"
#         )
#         self.assertResponseHasErrors(response)
#         actual_msg = json.loads(response.content)["errors"][0]["message"]
#         self.assertEqual(actual_msg, "No address or kvhx specified")
#
#     def test_address_input(self):
#         response = self.query(
#             """{
#             house(addressInput: "Kjærmarken 103, 6771 gredstedbro"){
#                 waterRisk {
#                   hollowing {
#                     image
#                   }
#                 }
#               }
#             }
#         """
#         )
#         house = json.loads(response.content)["data"]["house"]
#         self.assertResponseNoErrors(response)
#         self.assertEqual(type(house["waterRisk"]["hollowing"]["image"]), str)
