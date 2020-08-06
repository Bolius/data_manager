import dash
import dash_core_components as dcc
import dash_html_components as html
import json
import numpy as np
from django_plotly_dash import DjangoDash
from numpy import arange
from plotly import graph_objs as go

from data_models.models import BBR, House, Municipality, categorical_fields
from data_models.models import integer_fields as scalar_fields

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = DjangoDash("HistogramVis", external_stylesheets=external_stylesheets)
build_years = arange(1800, 2020, 1)
municipalities = Municipality.objects.all()
houses = House.objects.all()


styles = {
    "pre": {
        "border": "thin lightgrey solid",
        "overflowX": "scroll",
        "margin": "auto",
        "width": "80%",
    }
}

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
                                    {"label": s, "value": s, "somedata": s}
                                    for s in scalar_fields
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
                                style={"margin": "auto"},
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
                        style={
                            "width": "33%",
                            "display": "inline-block",
                            "margin": "auto",
                        },
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
                                    {"label": muni.name, "value": muni.name}
                                    for muni in municipalities
                                ],
                                multi=True,
                                value=None,
                            ),
                        ],
                        style={"width": "33%"},
                    ),
                    html.Div(
                        [
                            html.P(
                                ["Vælg kategori"],
                                style={"textAlign": "center", "font  ": "bold"},
                            ),
                            dcc.Dropdown(
                                id="category-choice",
                                options=[
                                    {"label": c, "value": c} for c in categorical_fields
                                ],
                                value=categorical_fields[0],
                            ),
                        ],
                        style={"width": "33%"},
                    ),
                ],
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
                # id="hover-data",
                [
                    dcc.Markdown(
                        """
                    **Hold markøren over en søjle for at se information**
                """,
                        style={"width": "80%", "margin": "auto"},
                    ),
                    html.Pre(id="hover-data", style=styles["pre"]),
                ]
            ),
        ]
    )

    def get_sum(hs, category, type):
        _locals = locals()
        query = f"hs = hs.filter(buldings__{category}='{type}')"
        exec(
            query, globals(), _locals,
        )

        bbr = _locals.get("hs")
        return len(bbr)

    def get_hover_data(categories, house_filtered=None):
        if house_filtered is None:
            house_filtered = houses

        hover1 = np.array(categories)

        # Total number of houses for municipality
        hover2 = np.array([len(house_filtered)] * len(categories)).reshape(
            len(categories), 1
        )
        return np.append(hover1, hover2, axis=1)

    @app.callback(
        dash.dependencies.Output("indicator-graphic", "figure"),
        [
            dash.dependencies.Input("xaxis", "value"),
            dash.dependencies.Input("xaxis-type", "value"),
            dash.dependencies.Input("val-from-x", "value"),
            dash.dependencies.Input("val-to-x", "value"),
            dash.dependencies.Input("muni-choice", "value"),
            dash.dependencies.Input("category-choice", "value"),
        ],
    )
    def update_graph(xParam, xType, valFromX, valToX, muniChoice, categoryChoice):

        cats = BBR._meta.get_field(categoryChoice).choices
        # get each category
        x = [c[1] for c in cats]

        hover_data = get_hover_data(cats)

        data = [
            {
                "x": x,
                "y": [
                    get_sum(houses, categoryChoice, c[0]) / len(houses) * 100
                    for c in cats
                ],
                "type": "bar",
                "name": "Danmark",
                "customdata": hover_data,
            }
        ]

        if muniChoice is not None:
            for m in muniChoice:
                hs = House.objects.filter(municipality=municipalities.get(name=m))

                y = [get_sum(hs, categoryChoice, c[0]) / len(hs) * 100 for c in cats]

                hover_data = get_hover_data(cats, hs)
                data.append(
                    {"x": x, "y": y, "type": "bar", "name": m, "customdata": hover_data}
                )

        plot = {
            "data": data,
            "layout": go.Layout(
                xaxis={"title": "Byer", "gridcolor": "white", "gridwidth": 2},
                yaxis={
                    "title": "Procentdel",
                    "type": "linear" if xType == "Linear" else "log",
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

    @app.callback(
        dash.dependencies.Output("hover-data", "children"),
        [dash.dependencies.Input("indicator-graphic", "hoverData")],
    )
    def display_hover_data(hoverData):
        return json.dumps(hoverData, indent=2)
