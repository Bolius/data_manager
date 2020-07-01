from data_models.models import Municipality
from django.contrib.gis import admin

from .municipality_admin import MunicipalityAdmin

admin.site.register(Municipality, MunicipalityAdmin)
