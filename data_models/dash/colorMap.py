from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import geojson
import pandas as pd
from django_plotly_dash import DjangoDash
from data_models.models import Municipality
import plotly.express as px
from django.core.serializers import serialize


app = DjangoDash("colorMap")

scalar_fields = [
    "Gennemsnits pris",
    "Gennemsnits størrelse",
    "Gennemsnits alder",
    "Gennemsnits Radon",
    "...",
]

# mapbox_access_token = "pk.eyJ1IjoibWJwaGFtIiwiYSI6ImNqdDVqdGhwbjA2bjIzeW45dDR0MHl6bHAifQ.uxGVk7wDQmmOiwGS15ebjQ"

df = pd.DataFrame({"x": [1, 2, 3], "SF": [4, 1, 2], "Montreal": [2, 4, 5]})

fig = px.bar(df, x="x", y=["SF", "Montreal"], barmode="group")


app.layout = html.Div(
    children=[
        html.Div(
            [
                html.P(
                    ["Farvelæg efter"], style={"textAlign": "left", "font  ": "bold"}
                ),
                dcc.Dropdown(
                    id="color-by",
                    options=[{"label": i, "value": i} for i in scalar_fields],
                    value=scalar_fields[0],
                ),
            ],
            style={"width": "80%", "margin-left": "auto", "margin-right": "auto"},
        ),
        dcc.RadioItems(
            id="cum-or-avg",
            options=[
                {"label": "Gennemsnit", "value": "avg"},
                {"label": "Median", "value": "cum"},
            ],
            value="cum",
            labelStyle={"display": "block"},
            style={"textAlign": "center"},
        ),
        html.Div(
            [html.Pre(id="hover-data")],
            style={
                "width": "80%",
                "margin-left": "auto",
                "margin-right": "auto",
                "margin-top": "20px",
            },
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
                dcc.Graph(
                    id="color-map",
                    config={"scrollZoom": True},
                    style={"height": "600px"},
                ),
            ],
            style={
                "width": "100%",
                "height": "800px",
                "margin-left": "auto",
                "margin-right": "auto",
            },
        ),
    ]
)


data = geojson.loads(
    serialize(
        "geojson",
        Municipality.objects.all(),
        geometry_field="geo_boundary",
        fields=("name", "admin_code"),
    )
)


@app.callback(Output("color-map", "figure"), [Input("cum-or-avg", "value")])
def update_graph(graph_type):
    fig = px.choropleth_mapbox(
        [
            {"admin_code": m.admin_code, "val": int(m.admin_code)}
            for m in Municipality.objects.all()
        ],
        geojson=data,
        color="val",
        locations="admin_code",
        featureidkey="properties.admin_code",
        center={"lat": 56.5331075, "lon": 11.8389737},
        mapbox_style="carto-positron",
        zoom=4.95,
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig
