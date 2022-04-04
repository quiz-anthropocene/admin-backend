from django.contrib.auth.admin import UserAdmin

from core.admin import admin_site
from users.models import User


class UserAdmin(UserAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "created",
    )
    list_filter = ["is_staff"]
    ordering = ["-created"]

    readonly_fields = ["is_active", "is_staff", "is_superuser", "last_login", "created", "updated"]
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        ("Dates", {"fields": ("last_login", "created", "updated")}),
    )
    add_fieldsets = ((None, {"fields": ("first_name", "last_name", "email", "password1", "password2")}),)


admin_site.register(User, UserAdmin)
