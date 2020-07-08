import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash

from data_models.models import BBR

data = BBR.get_time_data()
rolling_data = BBR.get_rolling_avgs()


def categorical_to_traces(categorical, time_range, field):
    traces = []
    for key in categorical[0]:
        traces.append(
            {
                "type": "scatter",
                "visible": "legendonly",
                "x": time_range,
                "y": [val[key] for val in categorical],
                "name": [
                    name
                    for (val, name) in BBR._meta.get_field(field).choices
                    if val == key
                ][0],
            }
        )
    return traces


def get_accumulated_figure():
    fig = {
        "data": [
            {
                "type": "scatter",
                "x": data["time_range"],
                "y": data["houses_per_year"],
                "name": "Antal bygninger",
            },
            {
                "type": "scatter",
                "visible": "legendonly",
                "x": data["time_range"],
                "y": data["recon_per_year"],
                "name": "Antal renoveringer",
            },
        ],
        "layout": {
            "showlegend": True,
            "xaxis": {"title": "Årstal", "type": "linear"},
            "yaxis": {"title": "Akkummuleret Antal", "type": "linear"},
            "title": "Akkummuleret antal over tid",
        },
    }
    fig["data"].extend(
        categorical_to_traces(
            BBR.accumulated_sum_for_catatgorical(
                "kitchen_facility", data["time_range"][0], data["time_range"][-1]
            ),
            data["time_range"],
            "kitchen_facility",
        )
    )
    fig["data"].extend(
        categorical_to_traces(
            BBR.accumulated_sum_for_catatgorical(
                "heat_install", data["time_range"][0], data["time_range"][-1]
            ),
            data["time_range"],
            "heat_install",
        )
    )
    fig["data"].extend(
        categorical_to_traces(
            BBR.accumulated_sum_for_catatgorical(
                "roofing_material", data["time_range"][0], data["time_range"][-1]
            ),
            data["time_range"],
            "roofing_material",
        )
    )
    fig["data"].extend(
        categorical_to_traces(
            BBR.accumulated_sum_for_catatgorical(
                "property_type", data["time_range"][0], data["time_range"][-1]
            ),
            data["time_range"],
            "property_type",
        )
    )
    return fig


def get_rolling_figure():
    return {
        "data": [
            {
                "type": "scatter",
                "x": rolling_data["time_range"],
                "y": rolling_data["bulding_area"],
                "name": "Bygnings størrelse",
            },
            {
                "type": "scatter",
                "visible": "legendonly",
                "x": rolling_data["time_range"],
                "y": rolling_data["garage_area"],
                "name": "Garage størrelse",
            },
            {
                "type": "scatter",
                "visible": "legendonly",
                "x": rolling_data["time_range"],
                "y": rolling_data["outhouse_area"],
                "name": "Størrelse udhus",
            },
            {
                "type": "scatter",
                "visible": "legendonly",
                "x": rolling_data["time_range"],
                "y": rolling_data["ground_area"],
                "name": "Grundes størrelse",
            },
            {
                "type": "scatter",
                "visible": "legendonly",
                "x": rolling_data["time_range"],
                "y": rolling_data["num_toilets"],
                "name": "Antal badeværelser",
            },
            {
                "type": "scatter",
                "visible": "legendonly",
                "x": rolling_data["time_range"],
                "y": rolling_data["num_rooms"],
                "name": "Antal Rum",
            },
            {
                "type": "scatter",
                "visible": "legendonly",
                "x": rolling_data["time_range"],
                "y": rolling_data["num_floors"],
                "name": "Antal etager",
            },
        ],
        "layout": {
            "showlegend": True,
            "xaxis": {"title": "Årstal", "type": "linear"},
            "yaxis": {"title": "Rullende gennemsnit", "type": "linear"},
            "title": "Rullende gennemsnit (5år) over tid",
        },
    }


app = DjangoDash("TimeVisualiser")
app.layout = html.Div(
    children=[
        html.H1(children="Se udviklingen af data over tid"),
        html.Div(
            children="""
            Du kan enten vælge at se data akkummuleret over tid, eller et
            rullende gennemsnit over data'en"""
        ),
        dcc.Graph(
            id="time-graph", figure=get_accumulated_figure(), style={"height": "600px"},
        ),
        dcc.RadioItems(
            id="cum-or-avg",
            options=[
                {"label": "Rullende gennemsnit", "value": "avg"},
                {"label": "Akkummuleret værdier", "value": "cum"},
            ],
            value="cum",
            labelStyle={"display": "block"},
            style={"textAlign": "center"},
        ),
    ],
)


@app.callback(Output("time-graph", "figure"), [Input("cum-or-avg", "value")])
def update_graph(graph_type):
    return get_rolling_figure() if graph_type == "avg" else get_accumulated_figure()
