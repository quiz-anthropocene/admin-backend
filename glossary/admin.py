from django.contrib import admin

from core.admin import ExportMixin, admin_site
from glossary.models import GlossaryItem


class GlossaryAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "definition_short",
        "created",
    )

    readonly_fields = ["created", "updated"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin_site.register(GlossaryItem, GlossaryAdmin)
