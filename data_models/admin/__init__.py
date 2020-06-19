from django.contrib.gis import admin

from data_models.models import Municipality

from .municipality_admin import MunicipalityAdmin

admin.site.register(Municipality, MunicipalityAdmin)
