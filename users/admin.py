from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.admin import admin_site
from users import constants
from users.models import AuthorDetail, User


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


class HasAuthorDetailFilter(admin.SimpleListFilter):
    title = "Author detail ?"
    parameter_name = "has_author_detail"

    def lookups(self, request, model_admin):
        return (("Yes", "Yes"), ("No", "No"))

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Yes":
            return queryset.has_author_detail()
        elif value == "No":
            return queryset.filter(author_detail__isnull=True)
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
        # "has_author_detail",
        "last_login",
        "created",
    ]
    list_filter = [RoleFilter, HasAuthorDetailFilter, "is_staff"]
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
        "has_author_detail",
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
                    "has_author_detail",
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

    def has_author_detail(self, user):
        return user.has_author_detail

    has_author_detail.short_description = "Author detail"
    has_author_detail.boolean = True


class AuthorDetailAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "has_image_url",
        "has_short_biography",
        "has_quiz_relationship",
        "has_website_url",
        "created",
    ]

    readonly_fields = ["created", "updated"]
    autocomplete_fields = ["user"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("user")
        return qs

    def has_image_url(self, instance):
        return instance.has_image_url

    has_image_url.short_description = "Author image"
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
admin_site.register(AuthorDetail, AuthorDetailAdmin)
