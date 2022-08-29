import json
from datetime import datetime

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.html import mark_safe
from fieldsets_with_inlines import FieldsetsInlineMixin

from core.admin import ExportMixin, admin_site
from quizs.models import Quiz, QuizQuestion, QuizRelationship
from stats import constants
from stats.models import QuizAnswerEvent, QuizFeedbackEvent


class QuizQuestionInline(admin.StackedInline):
    model = QuizQuestion
    autocomplete_fields = ["question"]
    extra = 0


class QuizRelationshipFromInline(admin.StackedInline):  # TabularInline
    model = QuizRelationship
    verbose_name = "Quiz Relationship (sortant)"
    fk_name = "from_quiz"
    # autocomplete_fields = ["to_quiz"]
    extra = 0

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Hide the current quiz in the relationship form
        Doesn't work with autocomplete_fields
        """
        field = super(QuizRelationshipFromInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "to_quiz":
            if "object_id" in request.resolver_match.kwargs:
                current_quiz_id = int(request.resolver_match.kwargs["object_id"])
                # remove the current quiz from the list
                field.queryset = Quiz.objects.exclude(id=current_quiz_id)
                # remove the current quiz's relationship quizs
                current_quiz_from_relationships = QuizRelationship.objects.filter(
                    from_quiz__id=current_quiz_id
                ).values_list("to_quiz_id", flat=True)
                current_quiz_to_relationships = QuizRelationship.objects.filter(
                    to_quiz__id=current_quiz_id
                ).values_list("from_quiz_id", flat=True)
                field.queryset = field.queryset.exclude(
                    id__in=(list(current_quiz_from_relationships) + list(current_quiz_to_relationships))
                )
                # order queryset
                field.queryset = field.queryset.order_by("-id")
        return field

    def has_change_permission(self, request, obj=None):
        return False


class QuizRelationshipToInline(admin.StackedInline):  # TabularInline
    model = QuizRelationship
    verbose_name = "Quiz Relationship (entrant)"
    fk_name = "to_quiz"
    extra = 0
    max_num = 0

    # def has_add_permission(self, request, obj=None):
    #     return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class QuizAdmin(FieldsetsInlineMixin, ExportMixin, admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "question_count",
        "author",
        "authors_list_string",
        "tags_list_string",
        "difficulty_average",
        "has_audio",
        "answer_count_agg",
        "validation_status",
        "publish",
        "spotlight",
        "created",
    ]
    search_fields = ["name"]
    list_filter = ["publish", "spotlight", "has_audio", "author", "authors", "visibility", "language", "tags"]
    ordering = ["-id"]

    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ["author"]
    filter_horizontal = ["tags"]
    # inlines = [QuizQuestionInline, QuizRelationshipFromInline, QuizRelationshipToInline]
    readonly_fields = [
        "id",
        # "slug",
        "question_count",
        "difficulty_average",
        "questions_not_validated_string_html",
        "questions_categories_list_with_count_string",
        "questions_tags_list_with_count_string",
        "questions_authors_list_with_count_string",
        "show_image_background",
        "answer_count_agg",
        "like_count_agg",
        "dislike_count_agg",
        "duration_average_seconds",
        "duration_average_minutes_string",
        "publish_date",
        "validation_date",
        "created",
        "updated",
    ]
    actions = [
        "export_as_csv",
        "export_as_json",
        "export_as_yaml",
        "export_all_quiz_as_yaml",
    ]

    fieldsets_with_inlines = [
        (
            "Infos de base",
            {
                "fields": (
                    "id",
                    "name",
                    "slug",
                    "language",
                    "author",
                    "introduction",
                    "conclusion",
                )
            },
        ),
        (
            "Tags",
            {"fields": ("tags",)},
        ),
        QuizQuestionInline,
        (
            "Recap des questions",
            {
                "fields": (
                    "has_audio",
                    "question_count",
                    "difficulty_average",
                    "questions_not_validated_string_html",
                    "questions_categories_list_with_count_string",
                    "questions_tags_list_with_count_string",
                    "questions_authors_list_with_count_string",
                )
            },
        ),
        (
            "Image",
            {
                "fields": (
                    "image_background_url",
                    "show_image_background",
                )
            },
        ),
        (
            "Publique ou Privé ?",
            {"fields": ("visibility",)},
        ),
        (
            "Validation",
            {"fields": ("validation_status", "validator", "validation_date")},
        ),
        (
            "Prêt à être publié ? Toutes les questions doivent être au statut 'validé' !",
            {
                "fields": (
                    "publish",
                    "publish_date",
                    "spotlight",
                )
            },
        ),
        QuizRelationshipFromInline,
        QuizRelationshipToInline,
        (
            "Stats",
            {
                "fields": (
                    "answer_count_agg",
                    "like_count_agg",
                    "dislike_count_agg",
                    "duration_average_seconds",
                    "duration_average_minutes_string",
                )
            },
        ),
        ("Dates", {"fields": ("created", "updated")}),
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("author", "agg_stats")
        qs = qs.prefetch_related("tags", "questions")
        return qs

    def show_image_background(self, instance):
        if instance.image_background_url:
            return mark_safe(
                f'<a href="{instance.image_background_url}" target="_blank">'
                f'<img src="{instance.image_background_url}" title="{instance.image_background_url}" height=300 />'  # noqa
                f"</a>"
            )
        else:
            return mark_safe("<div>champ 'Quiz image background url' vide</div>")

    show_image_background.short_description = "L'image (cliquer pour agrandir)"

    def questions_not_validated_string_html(self, instance):
        return mark_safe(instance.questions_not_validated_string)

    questions_not_validated_string_html.short_description = "Questions pas encore validées"

    def get_readonly_fields(self, request, obj=None):
        """
        Slug field should only be editable:
        - when the quiz is just created
        - if the quiz is not published yet
        """
        if obj:
            if obj.publish:
                return self.readonly_fields + ["slug"]
        return self.readonly_fields

    def get_prepopulated_fields(self, request, obj=None):
        """
        get_readonly_fields() method has an impact on get_prepopulated_fields()
        """
        if obj:
            if obj.publish:
                return {}
        return self.prepopulated_fields

    def changelist_view(self, request, extra_context=None):
        """
        show chart of answers per day
        https://dev.to/danihodovic/integrating-chart-js-with-django-admin-1kjb

        Corresponding template in quizs/templates/admin/quizs/quiz/change_list.html
        """
        # custom form
        current_quiz_id = int(request.POST.get("quiz_id", Quiz.objects.first().id))
        current_field = str(request.POST.get("field", constants.AGGREGATION_QUIZ_FIELD_CHOICE_LIST[0]))
        current_scale = str(request.POST.get("scale", constants.AGGREGATION_SCALE_CHOICE_LIST[0]))

        # Aggregate answers per day
        # chart_data_query = QuizAnswerEvent.objects.extra(select={"day": "date(created)"}) # sqlite
        chart_data_model = (
            QuizAnswerEvent if current_field == constants.AGGREGATION_QUIZ_FIELD_CHOICE_LIST[0] else QuizFeedbackEvent
        )
        chart_data_query = chart_data_model.objects.for_quiz(quiz_id=current_quiz_id).agg_timeseries(
            scale=current_scale
        )

        chart_data_list = list(chart_data_query)

        # get answers since today
        if len(chart_data_list) and (str(chart_data_list[-1]["day"]) != str(datetime.now().date())):
            chart_data_list += [{"day": str(datetime.now().date()), "y": 0}]

        # Serialize and attach the chart data to the template context
        chart_data_json = json.dumps(chart_data_list, cls=DjangoJSONEncoder)
        extra_context = extra_context or {
            "chart_data": chart_data_json,
            "quiz_choice_list": Quiz.objects.all().order_by("id"),
            "current_quiz_id": current_quiz_id,
            "field_choice_list": constants.AGGREGATION_QUIZ_FIELD_CHOICE_LIST,
            "current_field": current_field,
            "scale_choice_list": constants.AGGREGATION_SCALE_CHOICE_LIST,
            "current_scale": current_scale,
        }

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        css = {"all": ("css/admin/extra.css",)}


class QuizRelationshipAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "from_quiz",
        "status",
        "to_quiz",
        "created",
    )
    list_filter = ("status",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin_site.register(Quiz, QuizAdmin)
admin_site.register(QuizRelationship, QuizRelationshipAdmin)
