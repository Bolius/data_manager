# import urllib
# from textwrap import dedent as d
#
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import geojson
# import pandas as pd
# import plotly.graph_objs as go
# from django_plotly_dash import DjangoDash
# from textwrap import dedent as d
# from data_models.models import Municipality
# from numpy import array
#
# from data_models.models import Municipality
# from data_models.models.categoricalMapper import categories
#
# # OPTIMIZE: avoid copy or find a way to make a new geojson object
# kommuner_json = "geo_data/kommuner.geojson"
# # with open(kommuner_json) as f:
# #     d = geojson.load(f)  # noqa TODO fix this
#
#
# def get_region(name_list):
#     """
#     d : json data to copy
#     name_list: list of municipalities
#     """
#
#     t = [
#         (d["features"][i].properties["KOMNAVN"] in name_list)
#         for i in range(len(d["features"]))
#     ]
#
#     retval = {
#         "type": "FeatureCollection",
#         "crs": {
#             "type": "name",
#             "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"},
#         },
#         "features": array(d["features"])[t],
#     }
#     return retval
#
#
# app = DjangoDash("colorMap")
# municipalities = Municipality.objects.all()
# scalar_fields = [
#     "avg_size",
#     "avg_nr_rooms",
#     "avg_build_year",
#     "subscript_email",
#     "subscript_garden",
#     "subscript_save_energy",
#     "subscript_climate",
#     "subscript_competition",
#     "subscript_cleaning",
# ]
#
# mapbox_access_token = "pk.eyJ1IjoibWJwaGFtIiwiYSI6ImNqdDVqdGhwbjA2bjIzeW45dDR0MHl6bHAifQ.uxGVk7wDQmmOiwGS15ebjQ"
#
# colorscale = [
#     [0.0, "#f7fbff"],
#     [0.05, "#ebf3fb"],
#     [0.1, "#deebf7"],
#     [0.15, "#d2e3f3"],
#     [0.2, "#c6dbef"],
#     [0.25, "#b3d2e9"],
#     [0.3, "#9ecae1"],
#     [0.4, "#85bcdb"],
#     [0.5, "#6baed6"],
#     [0.6, "#57a0ce"],
#     [0.7, "#4292c6"],
#     [0.75, "#3082be"],
#     [0.8, "#2171b5"],
#     [0.9, "#1361a9"],
#     [1.0, "#08519c"],
# ]
#
# styles = {"pre": {"border": "thin lightgrey solid", "overflowX": "scroll"}}
# kommune_text = [
#     getattr(m, "municipality_name")
#     # "<br>Huse ialt: "
#     # + str(getattr(m, "nr_houses"))
#     # + "<br>Kældre ialt: "
#     # + str(getattr(m, "basements"))
#     # + "<br>Gnst. størrelse: "
#     # + str(getattr(m, "avg_size"))
#     for m in municipalities
# ]
# kommune_shape = [getattr(m, "geo_shape") for m in municipalities]
# kommune_center_x = [s.centroid.x for s in kommune_shape]
# kommune_center_y = [s.centroid.y for s in kommune_shape]
#
#
# app.layout = html.Div(
#     children=[
#         html.Div(
#             [
#                 html.P(
#                     ["Farvelæg efter"], style={"textAlign": "left", "font  ": "bold"}
#                 ),
#                 dcc.Dropdown(
#                     id="color-by",
#                     options=[
#                         {"label": categories.get(i), "value": i} for i in scalar_fields
#                     ],
#                     value=scalar_fields[0],
#                 ),
#             ],
#             style={"width": "80%", "margin-left": "auto", "margin-right": "auto"},
#         ),
#         html.Div(
#             [html.Pre(id="hover-data")],
#             style={
#                 "width": "80%",
#                 "margin-left": "auto",
#                 "margin-right": "auto",
#                 "margin-top": "20px",
#             },
#         ),
#         html.Div(
#             [
#                 html.A(
#                     "Download Data",
#                     id="download-link",
#                     download="rawdata.csv",
#                     href="",
#                     target="_blank",
#                 ),
#                 dcc.Graph(id="color-map", config={"scrollZoom": True}),
#             ],
#             style={"width": "80%", "margin-left": "auto", "margin-right": "auto"},
#         ),
#     ]
# )
#
# """
# Update colormap
# """
#
#
# @app.callback(
#     dash.dependencies.Output("color-map", "figure"),
#     [dash.dependencies.Input("color-by", "value")],
# )
# def update_map(colorBy):
#     """
#     colorBy: the attribute to color by, chosen by the user
#     ### compute the colors of the municipalities
#     ## get the max value we want to color by
#     ## spread the colors out to the different values
#     ## get the municipality names and apply assign it to a multipolygon for each color
#     """
#     if "subscript" in colorBy:
#         max_houses = 100
#         # the max value is 100, since we want to show the result in percentages
#         values = [
#             getattr(m, colorBy) / getattr(m, "nr_houses")
#             if (getattr(m, colorBy) != 0)
#             else 0
#             for m in municipalities
#         ]
#         colors = []
#         for v in values:
#             if v == 0:
#                 colors.append(colorscale[0][1])
#             elif v > 1:
#                 colors.append(colorscale[len(colorscale) - 1][1])
#             else:
#                 colors.append(colorscale[int(v * len(colorscale) - 1)][1])
#     else:
#         max_houses = max([getattr(m, colorBy) for m in municipalities])
#
#         colors = [
#             colorscale[int(getattr(m, colorBy) / max_houses * len(colorscale) - 1)][1]
#             if (getattr(m, colorBy) != 0)
#             else colorscale[0][1]
#             for m in municipalities
#         ]
#
#     multipoly_mun = []
#     for c in colorscale:
#         cp = []
#         for i in range(len(colors)):
#             if colors[i] == c[1]:
#                 cp.append(getattr(municipalities[i], "name"))
#         multipoly_mun.append(cp)
#
#     """
#     return the figure object
#     """
#
#     plot = {
#         "data": [
#             go.Scattermapbox(
#                 lat=kommune_center_y,
#                 lon=kommune_center_x,
#                 text=kommune_text,
#                 mode="markers",
#                 hoverinfo="text",
#                 marker=dict(
#                     size=2,
#                     color=[0, int(max_houses / 2), max_houses],
#                     colorbar=dict(title="Farveskala"),
#                     colorscale=colorscale,
#                 ),
#             )
#         ],
#         "layout": go.Layout(
#             autosize=True,
#             height=800,
#             hovermode="closest",
#             mapbox=dict(
#                 layers=[
#                     dict(
#                         source=get_region(multipoly_mun[i]),
#                         type="fill",
#                         color=colorscale[i][1],
#                         opacity=0.9,
#                     )
#                     for i in range(len(multipoly_mun))
#                 ],
#                 accesstoken=mapbox_access_token,
#                 bearing=0,
#                 center=dict(lat=56, lon=10),
#                 pitch=0,
#                 zoom=5.2,
#                 style="light",
#             ),
#         ),
#     }
#
#     return plot
#
#
# @app.callback(
#     dash.dependencies.Output("hover-data", "children"),
#     [dash.dependencies.Input("color-map", "hoverData")],
# )
# def update_info(hoverData):
#     info = hoverData.get("points", "")[0].get("text", "").split("<br>")
#     muni = municipalities.filter(name=info[0])[0]
#
#     return [
#         html.H3(info[0] + " Kommune"),
#         html.Div(
#             [
#                 html.P("Antal ejendomme: " + str(getattr(muni, "nr_houses"))),
#                 html.P("Antal kældre: " + str(getattr(muni, "basements"))),
#             ],
#             style={"width": "30%", "float": "left"},
#         ),
#         html.Div(
#             [
#                 html.P("Tilmeldt - email: " + str(getattr(muni, "subscript_email"))),
#                 html.P("Tilmeldt - have: " + str(getattr(muni, "subscript_garden"))),
#                 html.P(
#                     "Tilmeldt - indeklima: " + str(getattr(muni, "subscript_climate"))
#                 ),
#                 html.P(
#                     "Tilmeldt - rengøring: " + str(getattr(muni, "subscript_cleaning"))
#                 ),
#                 html.P(
#                     "Tilmeldt - spar energi: "
#                     + str(getattr(muni, "subscript_save_energy"))
#                 ),
#             ],
#             style={"width": "30%", "float": "left"},
#         ),
#         html.Div([html.P("...")], style={"width": "30%", "float": "left"}),
#     ]
#
#
# @app.callback(
#     dash.dependencies.Output("download-link", "href"),
#     [dash.dependencies.Input("color-by", "value")],
# )
# def update_download_link(colorBy):
#     color_info = [getattr(m, colorBy) for m in municipalities]
#     muni_names = [getattr(m, "name") for m in municipalities]
#
#     dff = pd.DataFrame({"Kommune": muni_names, colorBy: color_info})
#     csv_string = dff.to_csv(encoding="utf-8")
#     csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
#     return csv_string
