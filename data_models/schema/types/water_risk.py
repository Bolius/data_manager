# import graphene
# import sys
#
# sys.path.append("data_models/notebooks/water_comes")
# import requests
#
# url = "https://exl9ly9iwa.execute-api.eu-central-1.amazonaws.com/Prod/flood-risk"
#
#
# class Hollowing(graphene.ObjectType):
#     class Meta:
#         description = "Lavnings risikoer"
#
#     image = graphene.String(
#         name="image",
#         description="Base64 indkodet PNG som viser huset og områder hvor der er lavning.",
#         required=True,
#     )
#     risk = graphene.String(
#         description="Risiko for oversvømmelse ved skybrud givet lavningen i området. ('low', 'high')",
#         required=True,
#     )
#     # value = graphene.Int(
#     #     name="housePercentage",
#     #     description="Procentdel af huset som ligger i en lavning.",
#     #     required=True,
#     # )
#     # area_value = graphene.Int(
#     #     name="areaPercentage",
#     #     description="Procentdel af grunden som ligger i en lavning.",
#     #     required=True,
#     # )
#
#
# class Fastning(graphene.ObjectType):
#     class Meta:
#         description = "Befæstelsesgrads risikort"
#
#     image = graphene.String(
#         name="image",
#         description="Base64 indkodet PNG som viser huset sammen med befæstelsesgraden i området",
#         required=True,
#     )
#
#     risk = graphene.String(
#         description="Risiko for oversvømmelse ved skybrud givet befæstelsesgraden i området ('low', 'medium', 'high')",
#         required=True,
#     )
#     value = graphene.Int(
#         description="Del af grunden, som ligger i område med høj befæstelsesgrad.",
#         required=True,
#     )
#
#
# class Conductivity(graphene.ObjectType):
#     class Meta:
#         description = "Den hydrauliske ledeevne i området"
#
#     value = graphene.Int(
#         description="Den hydrauliske ledeevne i området", required=True
#     )
#     risk = graphene.String(
#         description="Risiko for oversvømmelse ved stormflod givet den hydrauliske ledeevne ('low', 'medium' or 'high')",
#         required=True,
#     )
#
#
# class Flood(graphene.ObjectType):
#     class Meta:
#         description = "Risiko for stormflod"
#
#     risk = graphene.String(
#         description="Risiko niveau for stormflod (low, medium, high)", required=True
#     )
#
#
# class WaterRisk(graphene.ObjectType):
#     class Meta:
#         description = (
#             "Faktorer der påvirker oversvømmelsesrisikoen for huset.\n"
#             + "Bolius har bygget modellen på baggrund af data fra geo"
#             + "datastyrelsen og kortforsyningen."
#         )
#
#     hollowing = graphene.NonNull(Hollowing)
#     fastningDegree = graphene.NonNull(Fastning)
#     conductivity = graphene.NonNull(Conductivity)
#     flood = graphene.NonNull(Flood)
#
#     # x = graphene.Float(required=True, description="Længdegrad")
#     # y = graphene.Float(required=True, description="Breddegrad")
#     address = graphene.String(required=True, description="adresse")
#     id = graphene.String(required=True, description="id")
#     querystring = {"address": address, "unadr_bbrid": id, "": ""}
#     payload = ""
#     response = requests.request("GET", url, data=payload, params=querystring)
#     response = response.json()
#
#     def resolve_flood(parent, info):
#         return Flood(risk=parent.response["storm_flood"]["risk"])
#
#     def resolve_hollowing(parent, info):
#         return Hollowing(
#             image=parent.response["rain_risk"]["factors"]["hollowing"]["image"],
#             risk=parent.response["rain_risk"]["factors"]["hollowing"]["risk"],
#             # response['rain_risk']['factors']['hollowing']['house_percentage']*100,
#             # area_value=response['rain_risk']['factors']['hollowing']['area_percentage']
#         )
#
#     def resolve_fastningDegree(parent, info):
#         return Fastning(
#             image=parent.response["rain_risk"]["factors"]["fastning"]["image"],
#             risk=parent.response["rain_risk"]["factors"]["fastning"]["risk"],
#             value=parent.response["rain_risk"]["factors"]["fastning"]["value"],
#         )
#
#     def resolve_conductivity(parent, info):
#         return Conductivity(
#             value=parent.response["rain_risk"]["factors"]["conductivity"]["value"],
#             risk=parent.response["rain_risk"]["factors"]["conductivity"]["risk"],
#         )
