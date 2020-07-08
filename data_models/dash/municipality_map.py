import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
from data_models.models import Municipality

app = DjangoDash("municipality_map")

muni_stats = Municipality.get_stats()

fig = px.choropleth_mapbox(
    # [
    #     {"admin_code": m.admin_code, "val": int(m.admin_code)}
    #     for m in Municipality.objects.all()
    # ],
    muni_stats["data"],
    geojson=muni_stats["geo_data"],
    color="nr_houses",
    color_continuous_scale="Viridis",
    locations="admin_code",
    featureidkey="properties.admin_code",
    center={"lat": 56.5331075, "lon": 11.8389737},
    mapbox_style="carto-positron",
    labels={"nr_houses": "Antal huse", "name": "Kommune"},
    # text=lambda x: "hej",
    zoom=4.95,
)

app.layout = html.Div(
    children=[
        dcc.Markdown(
            """
        ## Kommunekort
        På denne side kan du se hvordan tendenser har udvikliet sig i hver
        kommune.
        """
        ),
        dcc.Graph(
            id="color-map",
            config={"scrollZoom": True},
            style={"height": "90%", "border": "1px solid grey"},
            figure=fig,
        ),
    ],
    style={
        "width": "100%",
        "height": "100%",
        "margin-left": "auto",
        "margin-right": "auto",
    },
)
