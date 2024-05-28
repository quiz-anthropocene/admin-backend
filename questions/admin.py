from io import StringIO

from django.conf import settings
from django.contrib import admin
from django.core import management
from django.utils.html import mark_safe
from fieldsets_with_inlines import FieldsetsInlineMixin
from import_export import fields, resources
from import_export.admin import ImportMixin
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from simple_history.admin import SimpleHistoryAdmin

from categories.models import Category
from core import constants as api_constants
from core.admin import ExportMixin, admin_site
from core.models import Configuration
from core.utils import notion
from questions.models import Question, QuestionRelationship
from quizs.models import Quiz
from tags.models import Tag


class QuestionResource(resources.ModelResource):
    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(Category, field="name"),
    )
    tags = fields.Field(column_name="tags", attribute="tags", widget=ManyToManyWidget(Tag, field="name"))
    quizs = fields.Field(
        column_name="quizs",
        attribute="quizs",
        widget=ManyToManyWidget(Quiz, field="name"),
    )

    def before_import_row(self, row, **kwargs):
        """
        - Notion.so adds a BOM identifier before each line
        And setting from_encoding = 'utf-8-sig' in the QuestionAdmin does not work
        So we need to fix the 'id' column
        - Issue with BooleanFields because Notion exports Yes/No
        """
        # 'id' field
        if "id" not in row:
            row["id"] = row["\ufeffid"]
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
        if not settings.DEBUG and not dry_run and not (result.totals["error"] or result.totals["invalid"]):  # noqa
            notion.add_import_stats_row(result.total_rows, result.totals["new"], result.totals["update"])
        super(QuestionResource, self).after_import(dataset, result, using_transactions, dry_run, **kwargs)

    class Meta:
        model = Question
        skip_unchanged = True
        report_skipped = False


class QuestionRelationshipFromInline(admin.StackedInline):  # TabularInline
    model = QuestionRelationship
    verbose_name = "Question Relationship (sortant)"
    fk_name = "from_question"
    # autocomplete_fields = ["to_question"]
    extra = 0

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Hide the current question in the relationship form
        Doesn't work with autocomplete_fields
        """
        field = super(QuestionRelationshipFromInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "to_question":
            if "object_id" in request.resolver_match.kwargs:
                current_question_id = int(request.resolver_match.kwargs["object_id"])
                # remove the current question from the list
                field.queryset = Question.objects.exclude(id=current_question_id)
                # remove the current question's relationship questions
                current_question_from_relationships = QuestionRelationship.objects.filter(
                    from_question__id=current_question_id
                ).values_list("to_question_id", flat=True)
                current_question_to_relationships = QuestionRelationship.objects.filter(
                    to_question__id=current_question_id
                ).values_list("from_question_id", flat=True)
                field.queryset = field.queryset.exclude(
                    id__in=(list(current_question_from_relationships) + list(current_question_to_relationships))
                )
                # order queryset
                field.queryset = field.queryset.order_by("-id")
        return field

    def has_change_permission(self, request, obj=None):
        return False


class QuestionRelationshipToInline(admin.StackedInline):  # TabularInline
    model = QuestionRelationship
    verbose_name = "Question Relationship (entrant)"
    fk_name = "to_question"
    extra = 0
    max_num = 0

    # def has_add_permission(self, request, obj=None):
    #     return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class QuestionAdmin(ImportMixin, ExportMixin, FieldsetsInlineMixin, SimpleHistoryAdmin):
    resource_class = QuestionResource
    list_display = [
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
        # "has_answer_source_accessible_url",
        # "has_answer_source_scientific_url",
        # "has_answer_image_url",
        # "answer_count_agg",
        # "answer_success_count_agg",
        # "answer_success_rate",
        "created",
    ]
    search_fields = ["id", "text"]
    list_filter = [
        "validation_status",
        "type",
        "category",
        "difficulty",
        "author",
        "visibility",
        "language",
        # "quizs",
        "tags",
    ]
    ordering = ["-id"]  # "answer_count_agg", "answer_success_rate",
    actions = [
        "export_as_csv",
        "export_as_json",
        "export_as_yaml",
        "export_all_question_as_yaml",
    ]

    autocomplete_fields = ["author", "validator"]
    filter_horizontal = ["tags"]
    readonly_fields = [
        "quizs_list_string",
        "show_answer_image",
        "answer_count_agg",
        "answer_success_count_agg",
        "answer_success_rate",
        "like_count_agg",
        "dislike_count_agg",
        "validation_date",
        "created",
        "updated",
    ]

    fieldsets_with_inlines = [
        (
            "Infos de base",
            {
                "fields": (
                    # "id",
                    "text",
                    "hint",
                    "type",
                    "difficulty",
                    "language",
                    "author",
                )
            },
        ),
        (
            "Catégorie & Tags",
            {
                "fields": (
                    "category",
                    "tags",
                )
            },
        ),
        (
            "Détails des réponses",
            {
                "fields": (
                    "answer_choice_a",
                    "answer_choice_b",
                    "answer_choice_c",
                    "answer_choice_d",
                    "answer_correct",
                    "has_ordered_answers",
                    "answer_explanation",
                    "answer_audio_url",
                    "answer_audio_url_text",
                    "answer_video_url",
                    "answer_video_url_text",
                    "answer_source_accessible_url",
                    "answer_source_accessible_url_text",
                    "answer_source_scientific_url",
                    "answer_source_scientific_url_text",
                    "answer_book_recommendation",
                    "answer_extra_info",
                )
            },
        ),
        (
            "Image",
            {
                "fields": (
                    "answer_image_url",
                    "show_answer_image",
                    "answer_image_url_text",
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
        QuestionRelationshipFromInline,
        QuestionRelationshipToInline,
        (
            "Stats",
            {
                "fields": (
                    "answer_count_agg",
                    "answer_success_count_agg",
                    "answer_success_rate",
                    "like_count_agg",
                    "dislike_count_agg",
                )
            },
        ),
        (
            "Legal",
            {
                "fields": (
                    "author_certify_necessary_rights",
                    "author_agree_commercial_use",
                )
            },
        ),
        ("Dates", {"fields": ("created", "updated")}),
    ]

    change_list_template = "admin/questions/question/change_list_with_import.html"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("category", "author", "validator", "agg_stats")
        qs = qs.prefetch_related("tags", "quizs")
        return qs

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

    def has_answer_source_accessible_url(self, instance):
        return instance.has_answer_source_accessible_url

    has_answer_source_accessible_url.short_description = "Lien"
    has_answer_source_accessible_url.boolean = True

    def has_answer_image_url(self, instance):
        return instance.has_answer_image_url

    has_answer_image_url.short_description = "Image"
    has_answer_image_url.boolean = True

    def show_answer_image(self, instance):
        if instance.answer_image_url:
            return mark_safe(
                f'<a href="{instance.answer_image_url}" target="_blank">'
                f'<img src="{instance.answer_image_url}" title="{instance.answer_image_url_text}" height=300 />'  # noqa
                f"</a>"
            )
        else:
            return mark_safe("<div>champ 'Answer image url' vide</div>")

    show_answer_image.short_description = "L'image (cliquer pour agrandir)"

    def changelist_view(self, request, extra_context=None):
        """
        Corresponding template in questions/templates/admin/questions/question/change_list_with_import.html
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
            notion_questions_import_response = notion_questions_import_response.split("\n")
            notion_questions_import_response = [
                elem.split("///") if ("///" in elem) else elem for elem in notion_questions_import_response
            ]

        extra_context = extra_context or {
            "configuration": Configuration.get_solo(),
            "notion_questions_import_scope_choices": notion_questions_import_scope_choices,
            "notion_questions_import_response": notion_questions_import_response,
        }

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


admin_site.register(Question, QuestionAdmin)
