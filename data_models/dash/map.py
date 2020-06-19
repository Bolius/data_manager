import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from numpy import array

from data_models.models import BBR, CategoricalBBR, House, NumericBBR

# import pandas as pd
# import urllib

mapbox_access_token = "pk.eyJ1IjoibWJwaGFtIiwiYSI6ImNqdDVqdGhwbjA2bjIzeW45dDR0MHl6bHAifQ.uxGVk7wDQmmOiwGS15ebjQ"
app = DjangoDash("MapVis")
houses = House.objects.all()

bbr = BBR.objects.all()
bbr_num = NumericBBR.objects.all()

category_fields = CategoricalBBR._meta.get_fields()
category_fields = [field.name for field in category_fields]
category_fields.remove("bbr")
category_fields.remove("id")

scalar_fields = NumericBBR._meta.get_fields()
scalar_fields = [field.name for field in scalar_fields]
scalar_fields.remove("bbr")
scalar_fields.remove("id")


if len(scalar_fields) > 0:
    app.layout = html.Div(
        children=[
            html.Div(
                [
                    html.P(
                        ["Farvelæg efter"], style={"textAlign": "left", "font": "bold"}
                    ),
                    dcc.Dropdown(
                        id="color-by",
                        options=[{"label": c, "value": c} for c in category_fields],
                        value=category_fields[0],
                    ),
                ],
                style={
                    "width": "80%",
                    "margin-left": "auto",
                    "margin-right": "auto",
                    "margin-bottom": "20px",
                },
            ),
            html.Div(
                [
                    html.P(
                        ["Filtrér efter"], style={"textAlign": "left", "font  ": "bold"}
                    ),
                    dcc.Dropdown(
                        id="val",
                        options=[{"label": s, "value": s} for s in scalar_fields],
                        value=scalar_fields[0],
                    ),
                    dcc.Input(
                        id="val-from", placeholder="fra ...", type="number", value="0"
                    ),
                    dcc.Input(
                        id="val-to",
                        placeholder="til ...",
                        type="number",
                        value="99999999",
                    ),
                ],
                style={"width": "80%", "margin-left": "auto", "margin-right": "auto"},
            ),
            html.Div(
                [
                    html.A(
                        "Download Data",
                        id="download-link",
                        download="rawdata.csv",
                        href="",
                        target="_blank",
                    ),
                    dcc.Graph(id="map-s", config={"scrollZoom": True}),
                    dcc.RangeSlider(
                        id="year--slider",
                        min=1850,
                        max=2020,
                        value=[1990],
                        updatemode="drag",
                        count=5,
                        step=5,
                        marks={
                            str(build_year): str(build_year)
                            for build_year in range(1850, 2020, 10)
                        },
                    ),
                ],
                style={"width": "80%", "margin-left": "auto", "margin-right": "auto"},
            ),
        ]
    )

    @app.callback(
        dash.dependencies.Output("map-s", "figure"),
        [
            dash.dependencies.Input("color-by", "value"),
            dash.dependencies.Input("val", "value"),
            dash.dependencies.Input("val-from", "value"),
            dash.dependencies.Input("val-to", "value"),
            dash.dependencies.Input("year--slider", "value"),
        ],
    )
    def update_map(colorBy, val, valFrom, valTo, yearValue):
        hs = houses.filter(
            bbr__construction_year__gte=yearValue[0],
            bbr__construction_year__lte=yearValue[0] + 5,
            bbr__bbr_categorical__residential_type="one_fam",
        )

        lon = array([getattr(h, "lon") for h in hs])
        lat = array([getattr(h, "lat") for h in hs])

        # color_by = array([getattr(h.bbr.bbr_categorical, colorBy) for h in hs])
        # cats = list(set(color_by))

        return {
            "data": [
                go.Scattermapbox(
                    lat=lat,  # [color_by == getattr(c, "name")],
                    lon=lon,  # [color_by == getattr(c, "name")],
                    # name=,
                    mode="markers",
                    opacity=0.5,
                    marker=go.scattermapbox.Marker(size=5, opacity=0.5),
                )
                # for c in cats
            ],
            "layout": go.Layout(
                autosize=True,
                height=1000,
                hovermode="closest",
                mapbox=go.layout.Mapbox(
                    accesstoken=mapbox_access_token,
                    bearing=0,
                    center=go.layout.mapbox.Center(lat=56, lon=10),
                    pitch=0,
                    zoom=6,
                    style="light",
                ),
            ),
        }

    @app.callback(
        dash.dependencies.Output("download-link", "href"),
        [
            dash.dependencies.Input("color-by", "value"),
            dash.dependencies.Input("val", "value"),
            dash.dependencies.Input("val-from", "value"),
            dash.dependencies.Input("val-to", "value"),
        ],
    )
    def update_download_link(colorBy, val, valFrom, valTo):
        # h = []
        # for house in houses:
        #     if getattr(house, val) >= int(valFrom) and getattr(house, val) <= int(
        #         valTo
        #     ):
        #         h.append(house)
        #
        # lon_lat = [house.to_lat_lon() for house in h]
        # t = [list(t) for t in zip(*lon_lat)]
        # t0 = array(t[0])
        #
        # dff = pd.DataFrame({"lat": t0, "lon": t0})
        # csv_string = dff.to_csv(encoding="utf-8")
        # csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return  # csv_string
