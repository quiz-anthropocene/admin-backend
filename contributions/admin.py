from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from contributions.models import Comment
from core import constants
from core.admin import ExportMixin, admin_site


class HasParentFilter(admin.SimpleListFilter):
    title = _("Parent?")
    parameter_name = "has_parent"

    def lookups(self, request, model_admin):
        return ("Yes", _("Yes")), ("No", _("No"))

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Yes":
            return queryset.has_parent()
        elif value == "No":
            return queryset.filter(parent=None)
        return queryset


class HasReplyFilter(admin.SimpleListFilter):
    title = _("Answered?")
    parameter_name = "has_replies_reply"

    def lookups(self, request, model_admin):
        return ("Yes", _("Yes")), ("No", _("No"))

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Yes":
            return queryset.has_replies_reply()
        elif value == "No":
            return queryset.prefetch_related("replies").exclude(replies__type=constants.COMMENT_TYPE_REPLY)
        return queryset


class CommentAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "author",
        "text",
        # "description",
        "has_parent_icon",
        # "question",
        # "quiz",
        "has_replies_reply_icon",
        "status",
        "published_icon",
        "created",
    )
    list_filter = ["type", HasParentFilter, HasReplyFilter, "status", "publish"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("author")
        return qs

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in obj._meta.fields]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin_site.register(Comment, CommentAdmin)
