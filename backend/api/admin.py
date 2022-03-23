import json
from io import StringIO
from datetime import datetime

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group, Permission, User
from django.core import management
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.html import mark_safe

from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from import_export.admin import ImportMixin
from fieldsets_with_inlines import FieldsetsInlineMixin

from core.admin import admin_site, ExportMixin
from core.models import Configuration
from api import constants as api_constants
from api import utilities_notion
from api.models import (
    Question,
    Category,
    Tag,
    Quiz,
    QuizQuestion,
    QuizRelationship,
    Contribution,
    Glossary,
)
from stats import constants
from stats.models import (
    QuizAnswerEvent,
    QuizFeedbackEvent,
)


class QuestionResource(resources.ModelResource):
    """"""

    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(Category, field="name"),
    )
    tags = fields.Field(
        column_name="tags", attribute="tags", widget=ManyToManyWidget(Tag, field="name")
    )
    quizzes = fields.Field(
        column_name="quizzes",
        attribute="quizzes",
        widget=ManyToManyWidget(Quiz, field="name"),
    )

    def before_import_row(self, row, **kwargs):
        """
        - Notion.so adds a BOM identifier before each line
        And setting from_encoding = 'utf-8-sig' in the QuestionAdmin does not work
        So we need to fix the 'id' column
        - added timestamp
        - Issue with BooleanFields because Notion exports Yes/No
        """
        # 'id' field
        if "id" not in row:
            row["id"] = row["\ufeffid"]
        # 'added' field
        if row["added"] == "":
            row["added"] = datetime.strptime(
                row["Created time"], "%b %d, %Y %I:%M %p"
            ).date()
        # boolean fields
        BOOLEAN_FIELDS = ["has_ordered_answers"]
        for boolean_field in BOOLEAN_FIELDS:
            row[boolean_field] = True if (row[boolean_field] == "Yes") else False

    def import_obj(self, instance, row, dry_run):
        """
        Manually manage M2M column
        - tags in an existing instance: get the row's comma-seperated tags, get their ids,
        check if they are different than the instance, and finally set them to the instance
        - tags in a new instance: check that the tags exist
        """
        self._m2m_updated = False
        # get tag_ids
        tag_ids = []
        tags = row.get("tags")
        if tags:
            tags_split = tags.split(",")
            tag_ids = Tag.objects.get_ids_from_name_list(tags_split)
        # compare
        if instance.id:
            if list(instance.tags.values_list("id", flat=True)) != tag_ids:
                instance.tags.set(tag_ids)
                self._m2m_updated = True
        super(QuestionResource, self).import_obj(instance, row, dry_run)

    def skip_row(self, instance, original):
        """
        Highlight row if M2M column was updated
        """
        if self._m2m_updated:
            return False
        return super(QuestionResource, self).skip_row(instance, original)

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        # result.totals: OrderedDict, keys: 'new', 'update', 'delete', 'skip', 'error', 'invalid'
        if (
            not settings.DEBUG
            and not dry_run
            and not (result.totals["error"] or result.totals["invalid"])
        ):  # noqa
            utilities_notion.add_import_stats_row(
                result.total_rows, result.totals["new"], result.totals["update"]
            )
        super(QuestionResource, self).after_import(
            dataset, result, using_transactions, dry_run, **kwargs
        )

    class Meta:
        model = Question
        skip_unchanged = True
        report_skipped = False


class QuestionAdmin(ImportMixin, ExportMixin, admin.ModelAdmin):
    resource_class = QuestionResource
    list_display = (
        "id",
        "text",
        "type",
        "category",
        "tags_list_string",
        "quizs_list_string",
        "difficulty",
        "author",
        "validation_status",
        # "has_answer_explanation",
        # "has_answer_accessible_url",
        # "has_answer_scientific_url",
        # "has_answer_image_url",
        "answer_count_agg",
        "answer_success_count_agg",
        "answer_success_rate",
    )
    search_fields = (
        "id",
        "text",
    )
    list_filter = (
        "type",
        "category",
        "difficulty",
        "author",
        "validation_status",
        "language",
        # "quizzes",
        "tags",
    )
    ordering = ("-id",)  # "answer_count_agg", "answer_success_rate",
    actions = [
        "export_as_csv",
        "export_as_json",
        "export_as_yaml",
        "export_all_question_as_yaml",
    ]
    filter_horizontal = ("tags",)
    readonly_fields = (
        "quizs_list_string",
        "show_answer_image",
        "answer_count_agg",
        "answer_success_count_agg",
        "answer_success_rate",
        "like_count_agg",
        "dislike_count_agg",
        # "created_at",
        # "updated_at",
    )

    change_list_template = "admin/api/question/change_list_with_import.html"

    def has_add_permission(self, request, obj=None):
        return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False

    # from_encoding = 'utf-8-sig'
    def get_import_formats(self):
        """
        Restrict import formats to csv only
        """
        formats = ImportMixin.formats[:1]
        return [f for f in formats if f().can_import()]

    def has_answer_explanation(self, instance):
        return instance.has_answer_explanation

    has_answer_explanation.short_description = "Explication"
    has_answer_explanation.boolean = True

    def has_answer_accessible_url(self, instance):
        return instance.has_answer_accessible_url

    has_answer_accessible_url.short_description = "Lien"
    has_answer_accessible_url.boolean = True

    def has_answer_image_url(self, instance):
        return instance.has_answer_image_url

    has_answer_image_url.short_description = "Image"
    has_answer_image_url.boolean = True

    def show_answer_image(self, instance):
        if instance.answer_image_url:
            return mark_safe(
                f'<a href="{instance.answer_image_url}" target="_blank">'
                f'<img src="{instance.answer_image_url}" title="{instance.answer_image_explanation}" height=300 />'  # noqa
                f"</a>"
            )
        else:
            return mark_safe("<div>champ 'Answer image url' vide</div>")

    show_answer_image.short_description = (
        "L'image du champ 'Answer image url' (cliquer pour agrandir)"
    )

    def changelist_view(self, request, extra_context=None):
        """
        Corresponding template in templates/admin/api/question/change_list_with_import.html
        """
        notion_questions_import_scope_choices = [
            (
                scope_value,
                scope_label,
                "notion_questions_scope_" + str(scope_value) + "_last_imported",
            )
            for (
                scope_value,
                scope_label,
            ) in api_constants.NOTION_QUESTIONS_IMPORT_SCOPE_CHOICES[:1]
        ]
        notion_questions_import_response = []

        if request.POST.get("run_import_questions_from_notion_script", False):
            out = StringIO()
            # scope = request.POST.get("run_import_questions_from_notion_script")
            # management.call_command("import_questions_from_notion", scope, stdout=out)
            management.call_command("import_questions_from_notion", stdout=out)
            notion_questions_import_response = out.getvalue()
            notion_questions_import_response = notion_questions_import_response.split(
                "\n"
            )
            notion_questions_import_response = [
                elem.split("///") if ("///" in elem) else elem
                for elem in notion_questions_import_response
            ]

        extra_context = extra_context or {
            "configuration": Configuration.get_solo(),
            "notion_questions_import_scope_choices": notion_questions_import_scope_choices,
            "notion_questions_import_response": notion_questions_import_response,
        }

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


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


class TagAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "question_count",
        "quiz_count",
    )
    search_fields = ("name",)
    ordering = ("name",)
    actions = [
        "export_as_csv",
        "export_as_json",
        "export_as_yaml",
        "export_all_tag_as_yaml",
    ]


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
        field = super(QuizRelationshipFromInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )
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
                    id__in=(
                        list(current_quiz_from_relationships)
                        + list(current_quiz_to_relationships)
                    )
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
    list_display = (
        "id",
        "name",
        "question_count",
        "author",
        "tags_list_string",
        "difficulty_average",
        "has_audio",
        "answer_count_agg",
        "created",
        "publish",
        "spotlight",
    )
    search_fields = ("name",)
    list_filter = (
        "publish",
        "spotlight",
        "has_audio",
        "author",
        "language",
        "tags",
    )
    ordering = ("-id",)
    prepopulated_fields = {"slug": ("name",)}
    filter_vertical = ("questions",)
    filter_horizontal = ("tags",)
    # inlines = [QuizQuestionInline, QuizRelationshipFromInline, QuizRelationshipToInline]
    readonly_fields = (
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
        "created",
        "updated",
    )
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
        QuizQuestionInline,
        (
            "Recap des questions",
            {
                "fields": (
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
            "Tags & images",
            {
                "fields": (
                    "tags",
                    "image_background_url",
                    "show_image_background",
                )
            },
        ),
        (
            "Prêt à être publié ? Toutes les questions doivent être au statut 'validé' !",
            {
                "fields": (
                    "has_audio",
                    "publish",
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
                    "created",
                    "updated",
                )
            },
        ),
    ]

    def show_image_background(self, instance):
        if instance.image_background_url:
            return mark_safe(
                f'<a href="{instance.image_background_url}" target="_blank">'
                f'<img src="{instance.image_background_url}" title="{instance.image_background_url}" height=300 />'  # noqa
                f"</a>"
            )
        else:
            return mark_safe("<div>champ 'Quiz image background url' vide</div>")

    show_image_background.short_description = (
        "L'image du champ 'Quiz image background url' (cliquer pour agrandir)"
    )

    def questions_not_validated_string_html(self, instance):
        return mark_safe(instance.questions_not_validated_string)

    questions_not_validated_string_html.short_description = (
        "Questions pas encore validées"
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Slug field should only be editable:
        - when the quiz is just created
        - if the quiz is not published yets
        """
        if obj:
            if obj.publish:
                return self.readonly_fields + ("slug",)
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

        Corresponding template in templates/admin/api/quiz/change_list.html
        """
        # custom form
        current_quiz_id = int(request.POST.get("quiz_id", Quiz.objects.first().id))
        current_field = str(
            request.POST.get("field", constants.AGGREGATION_QUIZ_FIELD_CHOICE_LIST[0])
        )
        current_scale = str(
            request.POST.get("scale", constants.AGGREGATION_SCALE_CHOICE_LIST[0])
        )

        # Aggregate answers per day
        # chart_data_query = QuizAnswerEvent.objects.extra(select={"day": "date(created)"}) # sqlite
        chart_data_model = (
            QuizAnswerEvent
            if current_field == constants.AGGREGATION_QUIZ_FIELD_CHOICE_LIST[0]
            else QuizFeedbackEvent
        )
        chart_data_query = chart_data_model.objects.for_quiz(
            quiz_id=current_quiz_id
        ).agg_timeseries(scale=current_scale)

        chart_data_list = list(chart_data_query)

        # get answers since today
        if len(chart_data_list) and (
            str(chart_data_list[-1]["day"]) != str(datetime.now().date())
        ):
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


class ContributionAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "text",
        "description",
        "created",
    )

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in obj._meta.fields]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class GlossaryAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "definition_short",
        "created",
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin_site.register(Question, QuestionAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Tag, TagAdmin)
admin_site.register(Quiz, QuizAdmin)
admin_site.register(QuizRelationship, QuizRelationshipAdmin)
admin_site.register(Contribution, ContributionAdmin)
admin_site.register(Glossary, GlossaryAdmin)

admin_site.register(User)
admin_site.register(Permission)
admin_site.register(Group)
