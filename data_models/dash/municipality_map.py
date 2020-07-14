import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from data_models.models import Municipality

app = DjangoDash("municipality_map")

muni_stats = Municipality.get_stats()


fig = go.Figure(
    go.Choroplethmapbox(
        geojson=muni_stats["geo_data"],
        locations=muni_stats["data"].admin_code,
        z=muni_stats["data"]["average_age"],
        colorscale="Viridis",
        marker_opacity=0.5,
        marker_line_width=0,
        featureidkey="properties.admin_code",
        colorbar_title_text="Antal huse",
        hovertemplate="%{properties.name}<br />Antal Huse: %{z}<extra></extra>",
    )
)
fig.update_layout(
    title="Kommunekort",
    mapbox_style="carto-positron",
    mapbox_zoom=5.8,
    mapbox_center={"lat": 56.1331075, "lon": 11.8389737},
    margin={"l": 20, "r": 20, "t": 30, "b": 20},
)

paramter_mapping = {
    "average_size": "Gennemsnits størrelse",
    "average_age": "Gennemsnits alder",
    "nr_houses": "Antal huse",
}

app.layout = html.Div(
    children=[
        dcc.Graph(
            id="color-map",
            config={"scrollZoom": True},
            style={"height": "100%"},
            figure=fig,
        ),
        dcc.Dropdown(
            id="paramater-dropdown",
            options=[
                {"label": paramter_mapping[key], "value": key}
                for key in paramter_mapping
            ],
            value="nr_houses",
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
    Output("color-map", "figure"), [Input("paramater-dropdown", "value")],
)
def update_output(value):
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=muni_stats["geo_data"],
            locations=muni_stats["data"].admin_code,
            z=muni_stats["data"][value],
            colorscale="Viridis",
            marker_opacity=0.5,
            marker_line_width=0,
            featureidkey="properties.admin_code",
            colorbar_title_text=paramter_mapping[value],
            hovertemplate="Kommune: %{properties.name}<br />"
            + paramter_mapping[value]
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
