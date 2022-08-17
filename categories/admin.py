from django.contrib import admin

from categories.models import Category
from core.admin import ExportMixin, admin_site


class CategoryAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "name_long",
        "question_count",
        "question_public_validated_count",
    )
    search_fields = ("name",)
    ordering = ("id",)
    actions = [
        "export_as_csv",
        "export_as_json",
        "export_as_yaml",
        "export_all_category_as_yaml",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related("questions")
        return qs


admin_site.register(Category, CategoryAdmin)
