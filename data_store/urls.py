from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import RedirectView
from graphene_django.views import GraphQLView

from data_models.dash.map import app as MapVis  # noqa
from data_models.dash.scatter import app as ScatterVis  # noqa
from data_models.dash.histogram import app as HistogramVis  # noqa

# from django.core.management import call_command


from data_models.views import (  # predict_improvements,; predict_params,; add_session,; scatter,; map,; time,; colorMap,; mapView,; address_view,
    TimeView,
    MunicipalityMapView,
    EntryPage,
    scatter,
    map,
    address_view,
    HistogramView,
)

# """ A dirty hack around plotly loading apps before migrations are applied """
# with open("/tmp/migrate_status", "w") as f:
#     call_command("showmigrations", stdout=f)
# with open("/tmp/migrate_status", "r") as f:
#     lines = " ".join(f.readlines())
# if "[ ]" not in lines:
#     from data_models.dash.scatter import app as app1  # noqa
#     from data_models.dash.colorMap import app as app2  # noqa


urlpatterns = [
    path("django_plotly_dash/", include("django_plotly_dash.urls")),
    path("favicon.ico", RedirectView.as_view(url=settings.STATIC_URL + "favicon.ico")),
    path("admin/", admin.site.urls),
    path("", EntryPage, name="entry_page"),
    path("scatter", scatter, name="scatter"),
    path("visualizer/map", map, name="map_visualiser"),
    path("visualizer/time", TimeView, name="time_visualiser"),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=False))),
    path(r"address/", address_view, name="address"),
    path(r"address/<address>", address_view, name="addressInfo"),
    path("visualizer/municipalities", MunicipalityMapView, name="muni_map"),
    path("visualizer/histogram", HistogramView, name="hist_visualiser")
    # path(r"comfortscore/v2/addSession/", add_session, name="addSession"),
    # path(
    #     r"comfortscore/v2/predictParams/<address>/",
    #     predict_params,
    #     name="predictParams",
    # ),
    # path(
    #     r"comfortscore/v2/predictImprovements/<address>/",
    #     predict_improvements,
    #     name="predictImprovements",
    # ),
    # path(r"maps/<address>/", mapView, name="maps"),
    # path(r"maps/", mapView, name="maps"),
    # path(r"watercomes/<x>/<y>", water_comes, name="watercomes"),
]
