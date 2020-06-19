from django.contrib.gis.admin import GeoModelAdmin


class MunicipalityAdmin(GeoModelAdmin):
    fieldsets = [
        ("Info", {"fields": ["name", "admin_code"]}),
        ("Area", {"fields": ["geo_boundary"]}),
    ]
    readonly_fields = ["name", "admin_code"]
    modifiable = False
    list_display = (
        "name",
        "admin_code",
    )
