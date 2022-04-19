from django.contrib import admin

from core.admin import ExportMixin, admin_site
from tags.models import Tag


class TagAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "question_validated_count",
        "quiz_published_count",
    )
    search_fields = ("name",)
    ordering = ("name",)
    actions = [
        "export_as_csv",
        "export_as_json",
        "export_as_yaml",
        "export_all_tag_as_yaml",
    ]


admin_site.register(Tag, TagAdmin)
