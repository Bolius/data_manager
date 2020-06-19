""" Specifies which parts of the data models are visible in the admin UI """
import csv

from django.contrib import admin
from django.http import HttpResponse

from data_models.models import Action, House, Session


class ActionInline(admin.TabularInline):
    model = Action
    extra = 0


class SessionAdmin(admin.ModelAdmin):
    list_filter = ()
    readonly_fields = ("creation",)
    fieldsets = [
        ("Info", {"fields": ("creation",)}),  # FIX THIS 'house')}),
        (
            "Komfort parametre",
            {
                "fields": (
                    "original_draft",
                    "updated_draft",
                    "original_temperature",
                    "updated_temperature",
                    "original_moisture",
                    "updated_moisture",
                    "original_light",
                    "updated_light",
                    "original_noise",
                    "updated_noise",
                )
            },
        ),
    ]
    list_display = (
        "creation",
        "original_draft",
        "updated_draft",
        "original_temperature",
        "updated_temperature",
        "original_moisture",
        "updated_moisture",
        "original_light",
        "updated_light",
        "original_noise",
        "updated_noise",
    )
    inlines = [ActionInline]

    def export_param(self, request, queryset):
        meta = self.model._meta
        session_fields = [field.name for field in meta.fields]
        house_fields = [field.name for field in House._meta.fields]
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=params.csv"
        writer = csv.writer(response)
        writer.writerow(session_fields + house_fields)
        for obj in queryset:
            session_row = [getattr(obj, field) for field in session_fields]
            house_row = [getattr(obj.house, field) for field in house_fields]
            writer.writerow(session_row + house_row)
        return response

    def export_actions(self, request, queryset):
        action_fields = [field.name for field in Action._meta.fields]
        house_fields = [field.name for field in House._meta.fields]
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=actions.csv"
        writer = csv.writer(response)
        writer.writerow(action_fields + house_fields)
        for obj in queryset:

            for action in Action.objects.filter(session=obj):
                session_row = [getattr(action, field) for field in action_fields]
                house_row = [getattr(obj.house, field) for field in house_fields]
                writer.writerow(session_row + house_row)
        return response

    export_param.short_description = "Create CSV file with params and house"
    export_actions.short_description = "Create CSV file with action and house"
    actions = ["export_param", "export_actions"]


admin.site.register(Session, SessionAdmin)
