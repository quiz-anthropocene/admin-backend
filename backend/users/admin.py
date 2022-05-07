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
        "created",
    )
    list_filter = [RoleFilter, "is_staff"]
    search_fields = ["id", "first_name", "last_name", "email"]
    ordering = ["-created"]

    readonly_fields = ["is_active", "is_staff", "is_superuser", "last_login", "created", "updated"]
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
        ("Dates", {"fields": ("last_login", "created", "updated")}),
    )
    add_fieldsets = ((None, {"fields": ("first_name", "last_name", "email", "password1", "password2")}),)


admin_site.register(User, UserAdmin)
