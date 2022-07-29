from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.admin import admin_site
from users import constants
from users.models import User


class RoleFilter(admin.SimpleListFilter):
    title = User._meta.get_field("roles").verbose_name
    parameter_name = "roles"

    def lookups(self, request, model_admin):
        return constants.USER_ROLE_CHOICES

    def queryset(self, request, queryset):
        lookup_value = self.value()
        if lookup_value:
            if lookup_value == constants.USER_ROLE_CONTRIBUTOR:
                return queryset.all_contributors()
            if lookup_value == constants.USER_ROLE_SUPER_CONTRIBUTOR:
                return queryset.all_super_contributors()
            if lookup_value == constants.USER_ROLE_ADMINISTRATOR:
                return queryset.all_administrators()
        return queryset


class UserAdmin(UserAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "is_contributor",
        "is_super_contributor",
        "is_administrator",
        "question_count",
        "quiz_count",
        "last_login",
        "created",
    )
    list_filter = [RoleFilter, "is_staff"]
    search_fields = ["id", "first_name", "last_name", "email"]
    ordering = ["-created"]

    readonly_fields = [
        "is_contributor",
        "is_super_contributor",
        "is_administrator",
        "is_staff",
        "is_superuser",
        "last_login",
        "question_count",
        "quiz_count",
        "created",
        "updated",
    ]
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "roles",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (
            "Stats",
            {
                "fields": (
                    "question_count",
                    "quiz_count",
                )
            },
        ),
        ("Dates", {"fields": ("last_login", "created", "updated")}),
    )
    add_fieldsets = (
        (None, {"fields": ("first_name", "last_name", "email", "password1", "password2")}),
        ("Permissions", {"fields": ("roles",)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("questions", "quizs")

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def is_contributor(self, user) -> bool:
        return "✅" if user.has_role_contributor else "❌"

    is_contributor.short_description = "Contributeur ?"

    def is_super_contributor(self, user) -> bool:
        return "✅" if user.has_role_super_contributor else "❌"

    is_super_contributor.short_description = "Super-Contributeur ?"

    def is_administrator(self, user) -> bool:
        return "✅" if user.has_role_administrator else "❌"

    is_administrator.short_description = "Administrateur ?"

    def question_count(self, user):
        return user.question_count

    question_count.short_description = "Nbr de questions"
    question_count.admin_order_field = "question_count"

    def quiz_count(self, user):
        return user.quiz_count

    quiz_count.short_description = "Nbr de quizs"
    quiz_count.admin_order_field = "quiz_count"


admin_site.register(User, UserAdmin)
