from django.contrib import admin

from contributions.models import Comment
from core.admin import ExportMixin, admin_site


class CommentAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "text",
        "description",
        # "question",
        # "quiz",
        "author",
        "status",
        "created",
    )
    list_filter = ["type", "status"]

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in obj._meta.fields]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin_site.register(Comment, CommentAdmin)
