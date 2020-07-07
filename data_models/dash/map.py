import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from numpy import array

from data_models.models import BBR, House, categorical_fields
from data_models.models import integer_fields as scalar_fields

mapbox_access_token = "pk.eyJ1IjoibWJwaGFtIiwiYSI6ImNqdDVqdGhwbjA2bjIzeW45dDR0MHl6bHAifQ.uxGVk7wDQmmOiwGS15ebjQ"
app = DjangoDash("MapVis")
houses = House.objects.all()
bbr = BBR.objects.all()

if len(scalar_fields) > 0:
    app.layout = html.Div(
        children=[
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
                        id="val-to", placeholder="til ...", type="number", value="9999",
                    ),
                ],
                style={"width": "80%", "margin-left": "auto", "margin-right": "auto"},
            ),
            html.Div(
                [
                    html.P(
                        ["Sortér efter"], style={"textAlign": "left", "font  ": "bold"}
                    ),
                    dcc.Dropdown(
                        id="sort-by",
                        options=[{"label": c, "value": c} for c in categorical_fields],
                        value=categorical_fields[0],
                    ),
                ],
                style={"width": "80%", "margin-left": "auto", "margin-right": "auto"},
            ),
            html.Div(
                [
                    dcc.Graph(
                        id="map-s",
                        config={"scrollZoom": True},
                        style={"width": "1300px", "margin": "auto"},
                    ),
                    dcc.RangeSlider(
                        id="year--slider",
                        min=1850,
                        max=2020,
                        value=1990,
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

    def get_categorical(sortBy, choice, houses):
        _locals = locals()
        query = f"hs = houses.filter(buldings__{sortBy}= {choice})"
        exec(
            query, globals(), _locals,
        )

        houses = _locals.get("hs")
        data_points = array(houses.values_list("coordinates")).reshape(
            houses.count(), 2
        )
        return data_points

    @app.callback(
        dash.dependencies.Output("map-s", "figure"),
        [
            dash.dependencies.Input("val", "value"),
            dash.dependencies.Input("val-from", "value"),
            dash.dependencies.Input("val-to", "value"),
            dash.dependencies.Input("sort-by", "value"),
            dash.dependencies.Input("year--slider", "value"),
        ],
    )
    def update_map(val, valFrom, valTo, sortBy, yearValue):
        _locals = locals()
        query = f"hs = House.objects.filter(buldings__{val}__gte={valFrom}, buldings__{val}__lte={valTo})"

        exec(
            query, globals(), _locals,
        )

        houses = _locals.get("hs")
        choices = array(BBR._meta.get_field(sortBy).choices)

        return {
            "data": [
                go.Scattermapbox(
                    lat=get_categorical(sortBy, c[0], houses)[:, 1],
                    lon=get_categorical(sortBy, c[0], houses)[:, 0],
                    mode="markers",
                    name=c[1],
                    opacity=0.8,
                    marker=go.scattermapbox.Marker(size=6, opacity=0.8),
                )
                for c in choices
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
