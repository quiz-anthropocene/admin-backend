from django.contrib import admin

from categories.models import Category
from core.admin import ExportMixin, admin_site


class CategoryAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "name_long",
        "question_count",
    )
    search_fields = ("name",)
    ordering = ("id",)
    actions = [
        "export_as_csv",
        "export_as_json",
        "export_as_yaml",
        "export_all_category_as_yaml",
    ]


admin_site.register(Category, CategoryAdmin)
