import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
from plotly import graph_objs as go

from data_models.models import BBR
from data_models.visualizer.data_fetching import get_histogram_data

external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css"
]  # TODO Inline this?
HISTOGRAM_GRAPH = DjangoDash("HistogramVis", external_stylesheets=external_stylesheets)

graph_data = get_histogram_data()

styles = {
    "pre": {
        "border": "thin lightgrey solid",
        "overflowX": "scroll",
        "margin": "auto",
        "width": "50%",
    }
}

header = [
    html.Div(
        [
            html.P(["X"], style={"textAlign": "center", "font  ": "bold"}),
            dcc.Dropdown(
                id="xaxis",
                options=[
                    {"label": s, "value": s, "somedata": s} for s in BBR.integer_fields
                ],
                value=BBR.integer_fields[0],
            ),
            html.Div(
                [
                    dcc.Input(
                        id="val-from-x",
                        placeholder="fra ...",
                        type="number",
                        value="1",
                    ),
                    dcc.Input(
                        id="val-to-x",
                        placeholder="til ...",
                        type="number",
                        value="99999999",
                    ),
                ],
                style={"margin": "auto"},
            ),
            dcc.RadioItems(
                id="xaxis-type",
                options=[{"label": i, "value": i} for i in ["Linear", "Log"]],
                value="Linear",
                labelStyle={"display": "inline-block"},
            ),
        ],
        style={"width": "33%", "display": "inline-block", "margin": "auto"},
    ),
    html.Div(
        [
            html.P(
                ["Sammenlign kommuner"],
                style={"textAlign": "center", "font  ": "bold"},
            ),
            dcc.Dropdown(
                id="muni-choice",
                options=[
                    {"label": muni["name"], "value": muni["admin_code"]}
                    for muni in graph_data["municipalities"]
                ],
                multi=True,
                value=None,
            ),
        ],
        style={"width": "33%"},
    ),
    html.Div(
        [
            html.P(["Vælg kategori"], style={"textAlign": "center", "font  ": "bold"},),
            dcc.Dropdown(
                id="category-choice",
                options=[{"label": c, "value": c} for c in BBR.categorical_fields],
                value=BBR.categorical_fields[0],
            ),
        ],
        style={"width": "33%"},
    ),
]


HISTOGRAM_GRAPH.layout = html.Div(
    children=[
        html.Div(
            header,
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "width": "80%",
                "margin": "auto",
            },
        ),
        html.Div(
            [html.Div(id="table"), dcc.Graph(id="indicator-graphic",)],
            style={"width": "80%", "margin": "auto"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            "Hold markøren over en søjle for at se information",
                            style={"width": "80%", "margin": "auto"},
                        ),
                        html.Pre(id="hover-data"),
                    ],
                    style=styles["pre"],
                ),
                html.Div(
                    [
                        html.H6(
                            "Klik på en søjle for at se information",
                            style={"width": "80%", "margin": "auto"},
                        ),
                        html.Pre(id="click-data"),
                    ],
                    style=styles["pre"],
                ),
            ],
            style={"width": "80%", "display": "flex", "margin": "auto"},
        ),
    ]
)


@HISTOGRAM_GRAPH.callback(
    dash.dependencies.Output("indicator-graphic", "figure"),
    [
        dash.dependencies.Input("muni-choice", "value"),
        dash.dependencies.Input("category-choice", "value"),
    ],
)
def update_graph(muniChoice, categoryChoice):
    choices = BBR._meta.get_field(categoryChoice).choices

    buckets = [name for (_val, name) in choices]
    vals = [graph_data["denmark"][categoryChoice][key] for (key, name) in choices]
    fig_data = [{"x": buckets, "y": vals, "type": "bar", "name": "Danmark"}]

    if muniChoice is not None:
        for chosen_muni in muniChoice:
            y = [
                graph_data["municipalities_categories"][chosen_muni][categoryChoice][
                    key
                ]
                for (key, _name) in choices
            ]

            name = [
                muni["name"]
                for muni in graph_data["municipalities"]
                if muni["admin_code"] == chosen_muni
            ][0]
            fig_data.append({"x": buckets, "y": y, "type": "bar", "name": name})

    plot = {
        "data": fig_data,
        "layout": go.Layout(
            xaxis={"title": "Byer", "gridcolor": "white", "gridwidth": 3},
            yaxis={
                "title": "Procentdel",
                "gridcolor": "white",
                "gridwidth": 2,
                "range": [0, 100],
            },
            hovermode="closest",
            paper_bgcolor="rgb(243, 243, 243)",
            plot_bgcolor="rgb(243, 243, 243)",
        ),
    }
    return plot


@HISTOGRAM_GRAPH.callback(
    dash.dependencies.Output("hover-data", "children"),
    [dash.dependencies.Input("indicator-graphic", "hoverData")],
)
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


@HISTOGRAM_GRAPH.callback(
    dash.dependencies.Output("click-data", "children"),
    [dash.dependencies.Input("indicator-graphic", "clickData")],
)
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)
