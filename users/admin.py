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
    ordering = ["-created"]


admin_site.register(User, UserAdmin)
