import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from numpy import arange, array, unique

from data_models.models import BBR, CategoricalBBR, House, NumericBBR, City

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = DjangoDash("ScatterVis", external_stylesheets=external_stylesheets)
bbr = BBR.objects.all()

bbr_num = NumericBBR.objects.all()
bbr_categorical = CategoricalBBR.objects.all()
houses = House.objects.all()

build_years = arange(1800, 2020, 1)

scalar_fields = NumericBBR._meta.get_fields()
scalar_fields = [field.name for field in scalar_fields]
# scalar_fields.remove("bbr")
scalar_fields.remove("id")

category_fields = CategoricalBBR._meta.get_fields()
category_fields = [field.name for field in category_fields]
# category_fields.remove("bbr")
category_fields.remove("id")


citites = City.objects.all()

if len(scalar_fields) > 0:
    app.layout = html.Div(
        children=[
            html.Div(
                [
                    html.Div(
                        [
                            html.P(
                                ["Y"], style={"textAlign": "center", "font  ": "bold"}
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
                    html.Div(
                        [
                            html.P(
                                ["X"], style={"textAlign": "center", "font  ": "bold"}
                            ),
                            dcc.Dropdown(
                                id="yaxis",
                                options=[
                                    {"label": s, "value": s} for s in scalar_fields
                                ],
                                value=scalar_fields[1],
                            ),
                            html.Div(
                                [
                                    dcc.Input(
                                        id="val-from-y",
                                        placeholder="fra ...",
                                        type="number",
                                        value="1",
                                    ),
                                    dcc.Input(
                                        id="val-to-y",
                                        placeholder="til ...",
                                        type="number",
                                        value="99999999",
                                    ),
                                ],
                                style={"margin-left": "auto", "margin-right": "auto"},
                            ),
                            dcc.RadioItems(
                                id="yaxis-type",
                                options=[
                                    {"label": i, "value": i} for i in ["Linear", "Log"]
                                ],
                                value="Linear",
                                labelStyle={"display": "inline-block"},
                            ),
                        ],
                        style={
                            "width": "33%",
                            "float": "left",
                            "display": "inline-block",
                        },
                    ),
                    html.Div(
                        [
                            html.P(
                                ["Farvelæg efter"],
                                style={"textAlign": "center", "font  ": "bold"},
                            ),
                            dcc.Dropdown(
                                id="color_by",
                                options=[
                                    {"label": s, "value": s} for s in category_fields
                                ],
                                value=category_fields[0],
                            ),
                        ],
                        style={
                            "width": "33%",
                            "float": "right",
                            "display": "inline-block",
                        },
                    ),
                ],
                style={"width": "80%", "margin-left": "auto", "margin-right": "auto"},
            ),
            html.Div(
                id="description",
                style={"width": "80%", "margin-left": "auto", "margin-right": "auto"},
            ),
            html.Div(
                [
                    html.Div(id="table"),
                    # html.A(
                    #     "Download Data",
                    #     id="download-link",
                    #     download="rawdata.csv",
                    #     href="",
                    #     target="_blank",
                    # ),
                    dcc.Graph(id="indicator-graphic"),
                    html.H3("Årstal"),
                    dcc.RangeSlider(
                        id="year--slider",
                        min=min(build_years),
                        max=max(build_years),
                        value=[1820],
                        step=5,
                        marks={
                            str(build_year): str(build_year)
                            for build_year in range(
                                min(build_years), max(build_years) + 1, 10
                            )
                        },
                    ),
                ],
                style={"width": "80%", "margin-left": "auto", "margin-right": "auto"},
            ),
        ]
    )

    def get_size(count, max_count):
        return (count / max_count) * 100 if (count / max_count) * 100 > 0.1 else 8

    @app.callback(
        dash.dependencies.Output("indicator-graphic", "figure"),
        [
            dash.dependencies.Input("xaxis", "value"),
            dash.dependencies.Input("yaxis", "value"),
            dash.dependencies.Input("xaxis-type", "value"),
            dash.dependencies.Input("yaxis-type", "value"),
            dash.dependencies.Input("color_by", "value"),
            dash.dependencies.Input("val-from-x", "value"),
            dash.dependencies.Input("val-to-x", "value"),
            dash.dependencies.Input("val-from-y", "value"),
            dash.dependencies.Input("val-to-y", "value"),
            dash.dependencies.Input("year--slider", "value"),
        ],
    )
    def update_graph(
        yParam,
        xParam,
        yType,
        xType,
        colorBy,
        valFromX,
        valToX,
        valFromY,
        valToY,
        yearValue,
    ):
        # TODO: check security
        _locals = locals()

        if yParam == xParam:
            exec(
                f"hs = bbr.filter(bbr_numeric__{xParam}__gte={valFromY}, bbr_numeric__{xParam}__lte={valToY})",
                globals(),
                _locals,
            )
        else:
            exec(
                f"hs = bbr.filter(bbr_numeric__{xParam}__gte={valFromY}, bbr_numeric__{xParam}__lte={valToY}, bbr_numeric__{yParam}__gte={valFromX}, bbr_numeric__{yParam}__lte={valToX})",
                globals(),
                _locals,
            )
        bbr = _locals.get("hs")

        hs = bbr.filter(
            bbr_numeric__building_area__gt=10,
            bbr_numeric__building_area__lt=500,
            construction_year__gte=yearValue[0],
            construction_year__lte=yearValue[0] + 5,
        )

        if hs.exists():
            bbr_hs = array(hs.values_list("bbr_numeric_id")).flatten()

            scatter_points = array(
                bbr_num.filter(id__in=bbr_hs).values_list(xParam, yParam)
            )
            info, counts = unique(scatter_points, return_counts=True, axis=0)
        else:
            info = None
            counts = None

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

    @app.callback(
        dash.dependencies.Output("description", "children"),
        [
            dash.dependencies.Input("xaxis", "value"),
            dash.dependencies.Input("yaxis", "value"),
            dash.dependencies.Input("color_by", "value"),
        ],
    )
    def update_description(x, y, c):
        return
        # xd = getattr(Domain.objects.get(value=x), "description")
        # yd = getattr(Domain.objects.get(value=y), "description")
        # cd = getattr(Domain.objects.get(value=c), "description")
        # return [
        #     html.Div([html.P(yd)], style={'width': '33%', 'display': 'inline-block'}),
        #     html.Div([html.P(xd)], style={'width': '33%', 'display': 'inline-block'}),
        #     html.Div([html.P(cd)], style={'width': '33%', 'display': 'inline-block'})
        # ]

    # @app.callback(
    #     dash.dependencies.Output("download-link", "href"),
    #     [
    #         dash.dependencies.Input("xaxis", "value"),
    #         dash.dependencies.Input("yaxis", "value"),
    #         dash.dependencies.Input("color_by", "value"),
    #         dash.dependencies.Input("year--slider", "value"),
    #     ],
    # )
    # def update_download_link(yParam, xParam, colorBy, yearValue):
    #     return
    # hs = bbr.filter(
    #     construction_year__gte=yearValue[0], construction_year__lte=yearValue[1]
    # )
    # bbr_hs = array(hs.values_list("bbr_numeric_id")).flatten()
    # xaxis = array(bbr_num.filter(id__in=bbr_hs).values_list(xParam)).flatten()
    # yaxis = array(bbr_num.filter(id__in=bbr_hs).values_list(yParam)).flatten()
    #
    # bbr_cat = array(hs.values_list("bbr_categorical_id")).flatten()
    # color_by = array(
    #     bbr_categorical.filter(id__in=bbr_cat).values_list(colorBy)
    # ).flatten()
    #
    # dff = {xParam: xaxis, yParam: yaxis, colorBy: color_by}
    # dff = pd.DataFrame(dff)
    # csv_string = dff.to_csv(encoding="utf-8")
    # csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    # return csv_string
