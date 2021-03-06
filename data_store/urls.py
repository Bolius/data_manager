from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import RedirectView
from graphene_django.views import GraphQLView

from data_models.views import (
    EntryPage,
    HistogramView,
    MunicipalityMapView,
    TimeView,
    address_view,
    map,
    scatter,
)

urlpatterns = [
    path("django_plotly_dash/", include("django_plotly_dash.urls")),
    path("favicon.ico", RedirectView.as_view(url=settings.STATIC_URL + "favicon.ico")),
    path("admin/", admin.site.urls),
    path("", EntryPage, name="entry_page"),
    path("scatter", scatter, name="scatter"),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=False))),
    path(r"address/", address_view, name="address"),
    path(r"address/<address_id>", address_view, name="addressInfo"),
    path("visualizer/map", map, name="map_visualiser"),
    path("visualizer/time", TimeView, name="time_visualiser"),
    path("visualizer/municipalities", MunicipalityMapView, name="muni_map"),
    path("visualizer/histogram", HistogramView, name="hist_visualiser"),
]
