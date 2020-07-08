import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from numpy import arange

from data_models.models import BBR, Municipality
from data_models.models import integer_fields as scalar_fields, categorical_fields

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = DjangoDash("HistogramVis", external_stylesheets=external_stylesheets)
build_years = arange(1800, 2020, 1)
municipalities = Municipality.objects.all()
print(municipalities)
if len(scalar_fields) > 0:
    app.layout = html.Div(
        children=[
            html.Div(
                [
                    html.Div(
                        [
                            html.P(
                                ["X"], style={"textAlign": "center", "font  ": "bold"}
                            ),
                            dcc.Dropdown(
                                id="xaxis",
                                options=[
                                    {"label": s, "value": s} for s in scalar_fields
                                ],
                                value=scalar_fields[0],
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
                                style={"margin-left": "auto", "margin-right": "auto"},
                            ),
                            dcc.RadioItems(
                                id="xaxis-type",
                                options=[
                                    {"label": i, "value": i} for i in ["Linear", "Log"]
                                ],
                                value="Linear",
                                labelStyle={"display": "inline-block"},
                            ),
                        ],
                        style={"width": "33%", "display": "inline-block"},
                    ),
                ],
                style={"width": "80%", "margin-left": "auto", "margin-right": "auto"},
            ),
            html.Div(
                [html.Div(id="table"), dcc.Graph(id="indicator-graphic")],
                style={"width": "80%", "margin-left": "auto", "margin-right": "auto"},
            ),
        ]
    )

    def get_sum(category, type):
        _locals = locals()
        query = f"hs = BBR.objects.filter({category}={type})"
        exec(
            query, globals(), _locals,
        )

        bbr = _locals.get("hs")
        return len(bbr)

    @app.callback(
        dash.dependencies.Output("indicator-graphic", "figure"),
        [
            dash.dependencies.Input("xaxis", "value"),
            dash.dependencies.Input("xaxis-type", "value"),
            dash.dependencies.Input("val-from-x", "value"),
            dash.dependencies.Input("val-to-x", "value"),
        ],
    )
    def update_graph(xParam, xType, valFromX, valToX):
        data = []
        category = categorical_fields[0]
        cats = BBR._meta.get_field(category).choices

        x = [c[1] for c in cats]
        y = [get_sum(category, c[0]) for c in cats]

        plot = {
            "data": [{"x": x, "y": y, "type": "bar", "name": "SF"}],
            "layout": go.Layout(
                xaxis={"title": "Byer", "gridcolor": "white", "gridwidth": 2},
                yaxis={
                    "title": "Antal",
                    "type": "linear" if xType == "Linear" else "log",
                    "gridcolor": "white",
                    "gridwidth": 2,
                },
                hovermode="closest",
                paper_bgcolor="rgb(243, 243, 243)",
                plot_bgcolor="rgb(243, 243, 243)",
            ),
        }
        return plot
