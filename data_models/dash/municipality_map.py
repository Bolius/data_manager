import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from plotly import graph_objects as go

from data_models.models import BBR, Municipality

app = DjangoDash("municipality_map")

muni_stats = Municipality.get_stats()


app.layout = html.Div(
    children=[
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="map-dropdown",
                            options=[
                                {
                                    "label": BBR.field_to_desc(key),
                                    "value": key + "__avg",
                                }
                                for key in BBR.integer_fields
                            ],
                            value="construction_year__avg",
                            style={"width": "80%", "margin": "10px auto"},
                        ),
                        dcc.Graph(
                            id="color-map",
                            config={"scrollZoom": True},
                            style={"height": "100%"},
                        ),
                    ],
                    style={"height": "100%", "width": "70%"},
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="bar-dropdown",
                            options=[
                                {"label": BBR.field_to_desc(key), "value": key}
                                for key in BBR.categorical_fields
                            ],
                            value="heat_type",
                            style={"width": "80%", "margin": "10px auto"},
                        ),
                        dcc.Graph(
                            id="bar-chart",
                            config={"scrollZoom": True},
                            style={"height": "100%"},
                        ),
                    ],
                    style={"height": "100%", "width": "35%"},
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "height": "90%",
            },
        ),
    ],
    style={
        "width": "100%",
        "height": "100%",
        "margin-left": "auto",
        "margin-right": "auto",
    },
)


@app.callback(
    Output("color-map", "figure"), [Input("map-dropdown", "value")],
)
def update_output(value):
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=muni_stats["geo_data"],
            locations=muni_stats["data"].admin_code,
            z=muni_stats["muni_averages"][value],
            colorscale="Viridis",
            marker_opacity=0.5,
            marker_line_width=0,
            customdata=muni_stats["data"].name,
            featureidkey="properties.admin_code",
            colorbar_title_text=BBR.field_to_desc(value),
            hovertemplate="Kommune: %{properties.name}<br />"
            + BBR.field_to_desc(value)
            + ": %{z:.1f}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Kommunekort",
        mapbox_style="carto-positron",
        mapbox_zoom=5.8,
        mapbox_center={"lat": 56.1331075, "lon": 11.8389737},
        margin={"l": 20, "r": 20, "t": 30, "b": 20},
    )
    return fig


@app.callback(
    Output("bar-chart", "figure"),
    [Input("color-map", "clickData"), Input("bar-dropdown", "value")],
)
def update_bar(municipality, cat_field):
    if municipality is None:
        fig = go.Figure()
        fig.update_layout(
            title="Click på en kommune for at se data for den", font_color="red"
        )
        return fig
    muni_name = municipality["points"][0]["customdata"]
    municipality = municipality["points"][0]["location"]
    field_names = [
        BBR.choice_to_desc(cat_field, field[cat_field])
        for field in muni_stats["categorical"][municipality][cat_field]
    ]
    counts = [
        field["count"] for field in muni_stats["categorical"][municipality][cat_field]
    ]
    fig = go.Figure([go.Bar(x=field_names, y=counts)])
    fig.update_layout(
        title=f"Oversigt over {BBR.field_to_desc(cat_field)} for {muni_name}"
    )

    return fig
