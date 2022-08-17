from django.contrib import admin

from activity.models import Event
from core.admin import admin_site


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "actor_name",
        "event_verb",
        "event_object_type",
        "event_object_name",
        "created",
    )
    list_filter = (
        "event_object_type",
        "event_verb",
        "actor_name",
    )
    search_fields = (
        "actor_name",
        "event_object_type",
        "event_object_name",
    )
    ordering = ("-created",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin_site.register(Event, EventAdmin)
