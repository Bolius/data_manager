# from django.core.management import call_command
from django.core.management import call_command
from django.shortcuts import render

from data_models.models import House


def has_migrated():
    """ A dirty hack around plotly loading apps before migrations are applied """
    # TODO Make a better way for this
    with open("/tmp/migrate_status", "w") as f:
        call_command("showmigrations", stdout=f)
    with open("/tmp/migrate_status", "r") as f:
        lines = " ".join(f.readlines())
    return "[ ]" not in lines


if has_migrated():
    from data_models.visualizer import (  # noqa
        HISTOGRAM_GRAPH,
        MAP_GRAPH,
        MUNICIPALITY_GRAPH,
        SCATTER_GRAPH,
        TIME_GRAPH,
    )


def scatter(request):
    return render(request, "data_models/scatter.html")


def TimeView(request):
    return render(request, "data_models/time.html")


def map(request):
    return render(request, "data_models/map.html")


def MunicipalityMapView(request):
    return render(request, "data_models/municipality_map.html")


def HistogramView(request):
    return render(request, "data_models/histogram.html")


def address_enter(request):
    return render(request, "data_models/adressView.html", {})


def address_view(request, address_id=None):
    if address_id is None:
        print("In address_id is None")
        return render(request, "data_models/adressView.html", {})
        # query = settings.EXPLORATION_QUERY
        # query = query.replace("<address>", address_id)
        # query1 = settings.META_QUERY
        # # try:
        # schema = Schema(Query)
        # result = schema.execute(query)
        # meta = schema.execute(query1)
        # bbr_data = meta.data["house"]["fields"][3]["type"]["ofType"]["fields"]
        # water_comes_data = meta.data["house"]["fields"][2]["type"]["ofType"]["fields"]
        # radon_data = meta.data["house"]["fields"][4]["type"]["ofType"]["fields"]
        #
        # for i in range(len(bbr_data)):
        #     current_data = bbr_data[i]["name"]
        #     temp = result.data["house"]["bbrInfo"][current_data]
        #
        #     result.data["house"]["bbrInfo"][current_data] = {
        #         "value": temp,
        #         "description": bbr_data[i]["description"],
        #     }
        # for i in range(len(water_comes_data)):
        #     sub_data = water_comes_data[i]["type"]["ofType"]["fields"]
        #     sub_data_name = water_comes_data[i]["name"]
        #     try:
        #         for j in range(len(sub_data)):
        #             name = sub_data[j]["name"]
        #             temp = result.data["house"]["waterRisk"][sub_data_name][name]
        #             result.data["house"]["waterRisk"][sub_data_name][name] = {
        #                 "value": temp,
        #                 "description": sub_data[j]["description"],
        #             }
        #     except:  # noqa TODO fix this
        #         continue
        #
        # for i in range(len(radon_data)):
        #     current_data = radon_data[i]["name"]
        #     temp = result.data["house"]["radon"][current_data]
        #
        #     result.data["house"]["radon"][current_data] = {
        #         "value": temp,
        #         "description": radon_data[i]["description"],
        #     }
        #
        # hollow_img = result.data["house"]["waterRisk"]["hollowing"]["image"]["value"]
        # result.data["house"]["waterRisk"]["hollowing"]["image"]["value"] = (
        #     "data:image/jpeg;base64," + hollow_img[2:-1]
        # )
        #
        # fastningDegree_img = result.data["house"]["waterRisk"]["fastningDegree"][
        #     "image"
        # ]["value"]
        # result.data["house"]["waterRisk"]["fastningDegree"]["image"]["value"] = (
        #     "data:image/jpeg;base64," + fastningDegree_img[2:-1]
        # )
        # return render(request, "data_models/adressInfo.html", {"query_result": result})
        # # except:
        # #     # TODO: show error message
        # #     return render(request, "data_models/adressView.html", {})
    house = House.add_house(access_id=address_id)
    return render(request, "data_models/adressInfo.html", {"house": house})
