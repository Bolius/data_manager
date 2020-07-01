import dash
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash

from data_models.models import BBR, House

# from data_models.models import House, Domain, Category
# from numpy import array, cumsum
# import pandas as pd
# import urllib
# import plotly.graph_objs as go
d = dash
B = BBR

app = DjangoDash("TimeVisualiser")

app.layout = html.Div(
    children=[
        html.H1(children="Se udviklingen af data over tid"),
        html.Div(children="Hvis du savner data punkter giv, så giv endelig lyd"),
        dcc.Graph(
            id="example-graph",
            figure={
                "data": [
                    {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "SF"},
                    {"x": [1, 2, 3], "y": [2, 4, 5], "type": "bar", "name": "Montréal"},
                ],
                "layout": {"title": "Dash Data Visualization"},
            },
        ),
    ]
)


houses = House.objects.all()
build_years = sorted(
    list(
        set(
            [1992, 2018]
            # [
            #     house.bbr.construction_year
            #     for house in houses
            #     if house.bbr.construction_year != -1
            # ]
        )
    )
)

# category_fields = CategoricalBBR._meta.get_fields()
# category_fields = [field.name for field in category_fields]
# category_fields.remove("bbr")
# category_fields.remove("id")
#
# bbr = BBR.objects.all()
# bbr_categorical = CategoricalBBR.objects.all()

#
# app.layout = html.Div(
#     children=[
#         # html.Div(
#         #     [
#         #         dcc.Dropdown(
#         #             id="yaxis",
#         #             options=[
#         #                 {"label": getattr(c, "name"), "value": getattr(c, "value")}
#         #                 for c in category_fields
#         #             ],
#         #             value=getattr(category_fields[0], "value"),
#         #         ),
#         #         html.Div(id="table"),
#         #         html.A(
#         #             "Download Data",
#         #             id="download-link",
#         #             download="rawdata.csv",
#         #             href="",
#         #             target="_blank",
#         #         ),
#         #         dcc.RadioItems(
#         #             id="yaxis-type",
#         #             options=[{"label": i, "value": i} for i in ["Linear", "Log"]],
#         #             value="Linear",
#         #             labelStyle={"display": "inline-block"},
#         #         ),
#         #     ],
#         #     style={"width": "80%", "margin-left": "auto", "margin-right": "auto"},
#         # ),
#         html.Div(
#             id="description",
#             style={"width": "80%", "margin-left": "auto", "margin-right": "auto"},
#         ),
#         html.Div(
#             [dcc.Graph(id="indicator-graphic")],
#             style={"width": "80%", "margin-left": "auto", "margin-right": "auto"},
#         ),
#     ]
# )


# def get_acc(cat, cat_list, byear_list):
#     retval = []
#     for y in build_years:
#         # filter years
#         cats = cat_list[byear_list == y]
#         retval.append(len(cats[cats == cat]))
#     print(cumsum(retval))
#     return cumsum(retval)
#
#
# @app.callback(
#     dash.dependencies.Output("indicator-graphic", "figure"),
#     [
#         dash.dependencies.Input("yaxis", "value"),
#         dash.dependencies.Input("yaxis-type", "value"),
#     ],
# )
# def update_graph(yParam, yType):
#     # get the unique categories
#     domain = Domain.objects.get(value=yParam)
#     cats = Category.objects.filter(domain__value=yParam)
#     build_year = array(houses.values_list("build_year")).flatten()
#     cat = array(houses.values_list(yParam)).flatten()
#
#     return {
#         "data": [
#             go.Scatter(
#                 x=build_years,
#                 y=get_acc(getattr(c, "name"), cat, build_year),
#                 mode="markers+lines",
#                 opacity=0.4,
#                 name=getattr(c, "value"),
#                 marker={"size": 3, "line": {"width": 0.5}},
#             )
#             for c in cats
#         ],
#         "layout": go.Layout(
#             xaxis={"title": "Byggeår", "type": "linear"},
#             yaxis={
#                 "title": "akkummuleret antal ejendomme",
#                 "type": "linear" if yType == "Linear" else "log",
#             },
#             hovermode="closest",
#             title="akkummuleret antal af " + getattr(domain, "name") + " over byggeår",
#         ),
#     }
#
#
# @app.callback(
#     dash.dependencies.Output("description", "children"),
#     [dash.dependencies.Input("yaxis", "value")],
# )
# def update_description(y):
#     yd = getattr(Domain.objects.get(value=y), "description")
#     return [html.Div([html.P(yd)])]
#
#
# @app.callback(
#     dash.dependencies.Output("download-link", "href"),
#     [
#         dash.dependencies.Input("yaxis", "value"),
#         dash.dependencies.Input("yaxis-type", "value"),
#     ],
# )
# def update_download_link(yParam, yType):
#     domain = Domain.objects.get(value=yParam)
#     cats = Category.objects.filter(domain__value=yParam)
#     build_year = array(houses.values_list("build_year")).flatten()
#     cat = array(houses.values_list(yParam)).flatten()
#
#     dff = pd.DataFrame({"Byggeår": build_years})
#
#     for c in cats:
#         df1 = get_acc(getattr(c, "name"), cat, build_year)
#         dff.insert(1, getattr(c, "value"), df1)
#     csv_string = dff.to_csv(encoding="utf-8")
#     csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
#     return csv_string
