from datetime import datetime
from io import StringIO

from django.conf import settings
from django.contrib import admin
from django.core import management
from django.utils.html import mark_safe
from import_export import fields, resources
from import_export.admin import ImportMixin
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from categories.models import Category
from core import constants as api_constants
from core.admin import ExportMixin, admin_site
from core.models import Configuration
from core.utils import notion
from questions.models import Question
from quizs.models import Quiz
from tags.models import Tag


class QuestionResource(resources.ModelResource):
    """"""

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
        - added timestamp
        - Issue with BooleanFields because Notion exports Yes/No
        """
        # 'id' field
        if "id" not in row:
            row["id"] = row["\ufeffid"]
        # 'added' field
        if row["added"] == "":
            row["added"] = datetime.strptime(row["Created time"], "%b %d, %Y %I:%M %p").date()
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
        # "answer_count_agg",
        # "answer_success_count_agg",
        # "answer_success_rate",
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
        # "quizs",
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

    change_list_template = "admin/questions/question/change_list_with_import.html"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("category").prefetch_related("tags", "quizs")

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

    show_answer_image.short_description = "L'image du champ 'Answer image url' (cliquer pour agrandir)"

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
