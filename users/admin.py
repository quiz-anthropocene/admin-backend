from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from core.admin import admin_site
from users import constants
from users.models import User, UserCard


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


class HasUserCardFilter(admin.SimpleListFilter):
    title = _("User card?")
    parameter_name = "has_user_card"

    def lookups(self, request, model_admin):
        return ("Yes", _("Yes")), ("No", _("No"))

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Yes":
            return queryset.has_user_card()
        elif value == "No":
            return queryset.filter(user_card__isnull=True)
        return queryset


class UserAdmin(UserAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "is_contributor",
        "is_super_contributor",
        "is_administrator",
        "question_count",
        "quiz_count",
        # "has_user_card",
        "last_login",
        "created",
    ]
    list_filter = [RoleFilter, HasUserCardFilter, "is_staff"]
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
        "has_user_card",
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
                    "has_user_card",
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
        qs = qs.prefetch_related("questions", "quizs")
        return qs

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

    def has_user_card(self, user):
        return user.has_user_card

    has_user_card.short_description = "User card"
    has_user_card.boolean = True


class UserCardAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "has_image_url",
        "has_short_biography",
        "has_quiz_relationship",
        "has_website_url",
        "created",
    ]

    autocomplete_fields = ["user"]
    readonly_fields = ["created", "updated"]
    fieldsets = (
        (None, {"fields": ("user", "image_url", "short_biography", "quiz_relationship", "website_url")}),
        ("Dates", {"fields": ("created", "updated")}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("user")
        return qs

    def get_readonly_fields(self, request, obj=None):
        """
        User field should only be editable on creation
        """
        if not obj:
            return self.readonly_fields
        return self.readonly_fields + ["user"]

    def has_image_url(self, instance):
        return instance.has_image_url

    has_image_url.short_description = "User image"
    has_image_url.boolean = True

    def has_short_biography(self, instance):
        return instance.has_short_biography

    has_short_biography.short_description = "Short biography"
    has_short_biography.boolean = True

    def has_quiz_relationship(self, instance):
        return instance.has_quiz_relationship

    has_quiz_relationship.short_description = "Quiz relationship"
    has_quiz_relationship.boolean = True

    def has_website_url(self, instance):
        return instance.has_website_url

    has_website_url.short_description = "Website"
    has_website_url.boolean = True


admin_site.register(User, UserAdmin)
admin_site.register(UserCard, UserCardAdmin)
