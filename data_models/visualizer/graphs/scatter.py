import dash
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
from numpy import arange
from plotly import graph_objs as go

from data_models.models import BBR

external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css"
]  # TODO inline this
SCATTER_GRAPH = DjangoDash("ScatterVis", external_stylesheets=external_stylesheets)

build_years = arange(1800, 2020, 1)  # TODO DEL THIS


SCATTER_GRAPH.layout = html.Div(
    children=[
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            ["Værdi langs X aksen"],
                            style={"textAlign": "center", "font  ": "bold"},
                        ),
                        dcc.Dropdown(
                            id="xaxis",
                            options=[
                                {"label": field, "value": field}
                                for field in BBR.integer_fields
                            ],
                            value=BBR.integer_fields[0],
                        ),
                        dcc.RadioItems(
                            id="xaxis-type",
                            options=[
                                {"label": i, "value": i} for i in ["Linear", "Log"]
                            ],
                            value="Linear",
                            labelStyle={"display": "inline-block", "padding": "5px"},
                            style={"textAlign": "center"},  # TODO styling
                        ),
                    ],
                    style={"width": "40%", "padding": "5px", "display": "inline-block"},
                ),
                html.Div(
                    [
                        html.P(
                            ["Værdi langs Y aksen"],
                            style={"textAlign": "center", "font  ": "bold"},
                        ),
                        dcc.Dropdown(
                            id="yaxis",
                            options=[
                                {"label": s, "value": s} for s in BBR.integer_fields
                            ],
                            value=BBR.integer_fields[1],
                        ),
                        dcc.RadioItems(
                            id="yaxis-type",
                            options=[
                                {"label": i, "value": i} for i in ["Linear", "Log"]
                            ],
                            value="Log",
                            labelStyle={"display": "inline-block", "padding": "5px"},
                            style={"textAlign": "center"},
                        ),
                    ],
                    style={"width": "40%", "padding": "5px", "display": "inline-block"},
                ),
            ],
            style={
                "width": "100%",
                "textAlign": "center",
                "display": "flex",
                "justifyContent": "center",
            },
        ),
        html.Div(
            [dcc.Graph(id="indicator-graphic")],
            style={"width": "90%", "margin-left": "auto", "margin-right": "auto"},
        ),
    ]
)


def get_size(count, max_count):
    return (count / max_count) * 100 if (count / max_count) * 100 > 0.1 else 8


@SCATTER_GRAPH.callback(
    dash.dependencies.Output("indicator-graphic", "figure"),
    [
        dash.dependencies.Input("xaxis", "value"),
        dash.dependencies.Input("yaxis", "value"),
        dash.dependencies.Input("xaxis-type", "value"),
        dash.dependencies.Input("yaxis-type", "value"),
    ],
)
def update_graph(xParam, yParam, xType, yType):

    info, counts = BBR.get_scatter_points(xParam, yParam, 0, 2000, 0, 2000, [1930])

    plot = {
        "data": [
            go.Scattergl(
                # get all points that is satisfying the category prop
                x=info[:, 0] if info is not None else [],
                y=info[:, 1] if info is not None else [],
                mode="markers",
                opacity=0.7,
                text=counts,
                marker_size=[get_size(c, max(counts)) for c in counts]
                if counts is not None
                else 0,
            )
        ],
        "layout": go.Layout(
            xaxis={
                "title": xParam,
                "type": "linear" if xType == "Linear" else "log",
                "gridcolor": "white",
                "gridwidth": 2,
            },
            yaxis={
                "title": yParam,
                "type": "linear" if yType == "Linear" else "log",
                "gridcolor": "white",
                "gridwidth": 2,
            },
            hovermode="closest",
            paper_bgcolor="rgb(243, 243, 243)",
            plot_bgcolor="rgb(243, 243, 243)",
            title=xParam,
        ),
    }
    return plot
