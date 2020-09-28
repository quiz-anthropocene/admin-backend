import csv
import json
from io import StringIO
from datetime import datetime

# from io import StringIO

from django.http import HttpResponse
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.core import management
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.html import mark_safe

from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from import_export.admin import ImportMixin, DEFAULT_FORMATS

# from django.core.management import call_command

from api import constants
from api import utilities, utilities_notion
from api.models import (
    Question,
    Category,
    Tag,
    Quiz,
    QuestionAnswerEvent,
    QuestionFeedbackEvent,
    QuestionAggStat,
    QuizAnswerEvent,
    QuizFeedbackEvent,
    DailyStat,
    Contribution,
    Glossary,
)


class ExportMixin:
    """
    Add export actions
    https://books.agiliq.com/projects/django-admin-cookbook/en/latest/export.html
    """

    def export_as_csv(self, request, queryset):
        """
        TODO: improve ManyToMany management (currently: hack to add tags to Question)
        """
        response = HttpResponse(content_type="text/csv")
        response[
            "Content-Disposition"
        ] = f"attachment; filename={self.model._meta} - {datetime.now().date()}.csv"

        # field_names = [field.name for field in self.model._meta.get_fields()]
        field_names = [field.name for field in self.model._meta.fields]

        writer = csv.writer(response)

        if queryset.model.__name__ == "Question":
            writer.writerow(field_names + ["tags"])
        else:
            writer.writerow(field_names)

        for obj in queryset:
            if queryset.model.__name__ == "Question":
                writer.writerow(
                    [getattr(obj, field) for field in field_names]
                    + [obj.tags_list_string]
                )
            else:
                writer.writerow([getattr(obj, field) for field in field_names])

        return response

    def export_as_json(self, request, queryset):
        response = HttpResponse(content_type="application/json")
        response[
            "Content-Disposition"
        ] = f"attachment; filename={self.model._meta} - {datetime.now().date()}.json"

        response.write(utilities.serialize_queryset_to_json(queryset))

        return response

    def export_as_yaml(self, request, queryset):
        """
        TODO: escape characters " (\") and - (\\-)
        """
        response = HttpResponse(content_type="text/yaml")
        response[
            "Content-Disposition"
        ] = f"attachment; filename={self.model._meta} - {datetime.now().date()}.yaml"

        response.write(utilities.serialize_queryset_to_yaml(queryset))

        return response

    def export_all_question_as_yaml(self, request, queryset):
        return self.export_as_yaml(request, Question.objects.all().order_by("pk"))

    def export_all_questionanswerevent_as_yaml(self, request, queryset):
        return self.export_as_yaml(
            request, QuestionAnswerEvent.objects.all().order_by("pk")
        )

    def export_all_questionfeedbackevent_as_yaml(self, request, queryset):
        return self.export_as_yaml(
            request, QuestionFeedbackEvent.objects.all().order_by("pk")
        )

    def export_all_quiz_as_yaml(self, request, queryset):
        return self.export_as_yaml(request, Quiz.objects.all().order_by("pk"))

    def export_all_category_as_yaml(self, request, queryset):
        return self.export_as_yaml(request, Category.objects.all().order_by("pk"))

    def export_all_tag_as_yaml(self, request, queryset):
        return self.export_as_yaml(request, Tag.objects.all().order_by("pk"))

    # def export_all_as_yaml(self, request):
    #     meta = self.model._meta

    #     response = HttpResponse(content_type='text/yaml')
    #     response['Content-Disposition'] = 'attachment; filename={}.yaml'.format(meta)

    #     out = StringIO()
    #     call_command('dumpdata', 'api.question', '--format=yaml', '--pretty', stdout=out)

    #     response.write(out.getvalue())

    #     return response

    export_as_csv.short_description = "Export Selected (CSV)"
    export_as_json.short_description = "Export Selected (JSON)"
    export_as_yaml.short_description = "Export Selected (YAML)"
    export_all_question_as_yaml.short_description = "Export All (YAML)"
    export_all_questionanswerevent_as_yaml.short_description = "Export All (YAML)"
    export_all_questionfeedbackevent_as_yaml.short_description = "Export All (YAML)"
    export_all_quiz_as_yaml.short_description = "Export All (YAML)"
    export_all_category_as_yaml.short_description = "Export All (YAML)"
    export_all_tag_as_yaml.short_description = "Export All (YAML)"


class QuestionResource(resources.ModelResource):
    """
    """

    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(Category, field="name"),
    )
    tags = fields.Field(
        column_name="tags", attribute="tags", widget=ManyToManyWidget(Tag, field="name")
    )

    def before_import_row(self, row, **kwargs):
        """
        - Notion.so adds a BOM identifier before each line
        And setting from_encoding = 'utf-8-sig' in the QuestionAdmin does not work
        So we need to fix the 'id' column
        - added timestamp
        - Issue with BooleanFields because Notion exports Yes/No
        - Fill 'publish' field
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
        BOOLEAN_FIELDS = ["has_ordered_answers"]  # "publish"
        for boolean_field in BOOLEAN_FIELDS:
            row[boolean_field] = True if (row[boolean_field] == "Yes") else False
        # 'publish' field
        row["publish"] = (
            True
            if (row["validation_status"] == constants.QUESTION_VALIDATION_STATUS_OK)
            else False
        )

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
        "difficulty",
        "author",
        "publish",
        # "validation_status",
        "has_answer_explanation",
        "has_answer_accessible_url",
        # "has_answer_scientific_url",
        "has_answer_image_url",
        "answer_count_agg",
        "answer_success_count_agg",
        "answer_success_rate",
    )
    list_filter = (
        "type",
        "category",
        "tags",
        "difficulty",
        "author",
        "publish",
        "validation_status",
    )
    ordering = ("id",)  # "answer_count_agg", "answer_success_rate",
    actions = [
        "export_as_csv",
        "export_as_json",
        "export_as_yaml",
        "export_all_question_as_yaml",
    ]
    filter_horizontal = ("tags",)
    readonly_fields = (
        "publish",  # True if status 'Validée'
        "show_answer_image",
        "answer_count_agg",
        "answer_success_count_agg",
        "answer_success_rate",
        "like_count_agg",
        "dislike_count_agg",
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
        formats = DEFAULT_FORMATS[:1]
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
    show_answer_image.allow_tags = True

    def changelist_view(self, request, extra_context=None):
        """
        Corresponding template in templates/admin/api/question/change_list_with_import.html
        """

        notion_questions_validation = []

        if request.POST.get("run_import_questions_from_notion_script", False):
            out = StringIO()
            scope = request.POST.get("run_import_questions_from_notion_script")
            management.call_command("import_questions_from_notion", scope, stdout=out)
            notion_questions_validation = out.getvalue()
            notion_questions_validation = notion_questions_validation.split("|||")

        extra_context = extra_context or {
            "notion_questions_validation": notion_questions_validation
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
    ordering = ("name",)
    actions = [
        "export_as_csv",
        "export_as_json",
        "export_as_yaml",
        "export_all_tag_as_yaml",
    ]


class QuizAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "question_count",
        "author",
        "tags_list_string",
        "difficulty_average",
        "publish",
        "answer_count_agg",
    )
    list_filter = ("publish",)
    ordering = ("name",)
    filter_horizontal = (
        "questions",
        "tags",
    )
    readonly_fields = (
        "show_image_background",
        "question_count",
        "questions_categories_list_string",
        "questions_tags_list_string",
        "difficulty_average",
        "answer_count_agg",
        "like_count_agg",
        "dislike_count_agg",
    )
    actions = [
        "export_as_csv",
        "export_as_json",
        "export_as_yaml",
        "export_all_quiz_as_yaml",
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
    show_image_background.allow_tags = True

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


class QuestionAnswerEventAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "question",
        "choice",
        "source",
        "created",
    )
    list_filter = ("source",)
    ordering = ("id",)
    actions = [
        "export_as_csv",
        "export_as_json",
        "export_as_yaml",
        "export_all_questionanswerevent_as_yaml",
    ]

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in obj._meta.fields]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        """
        show chart of answers per day
        https://dev.to/danihodovic/integrating-chart-js-with-django-admin-1kjb

        Corresponding template in templates/admin/api/questionanswerevent/change_list.html
        """
        # Aggregate answers per day
        chart_data_query = QuestionAnswerEvent.objects.agg_timeseries()

        chart_data_list = list(chart_data_query)

        # get answers since today
        if len(chart_data_list) and (
            str(chart_data_list[-1]["day"]) != str(datetime.now().date())
        ):
            chart_data_list += [{"day": str(datetime.now().date()), "y": 0}]

        # Serialize and attach the chart data to the template context
        chart_data_json = json.dumps(chart_data_list, cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": chart_data_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


class QuestionFeedbackEventAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "question",
        "choice",
        "source",
        "created",
    )
    list_filter = ("source",)
    ordering = ("id",)
    actions = [
        "export_as_csv",
        "export_as_json",
        "export_as_yaml",
        "export_all_questionfeedbackevent_as_yaml",
    ]

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in obj._meta.fields]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class QuestionAggStatAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "question_id",
        "answer_count",
        "answer_success_count",
        "like_count",
        "dislike_count",
    )

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in obj._meta.fields]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class QuizAnswerEventAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "quiz",
        "question_count",
        "answer_success_count",
        "created",
    )
    list_filter = ("quiz",)
    ordering = ("id",)
    actions = ["export_as_csv", "export_as_json", "export_as_yaml"]

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in obj._meta.fields] + ["question_count"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        """
        show chart of answers per day
        https://dev.to/danihodovic/integrating-chart-js-with-django-admin-1kjb

        Corresponding template in templates/admin/api/quizanswerevent/change_list.html
        """
        # Aggregate answers per day
        # chart_data_query = QuizAnswerEvent.objects.extra(select={"day": "date(created)"}) # sqlite
        chart_data_query = QuizAnswerEvent.objects.agg_timeseries()

        chart_data_list = list(chart_data_query)

        # get answers since today
        if len(chart_data_list) and (
            str(chart_data_list[-1]["day"]) != str(datetime.now().date())
        ):
            chart_data_list += [{"day": str(datetime.now().date()), "y": 0}]

        # Serialize and attach the chart data to the template context
        chart_data_json = json.dumps(chart_data_list, cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": chart_data_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


class QuizFeedbackEventAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "quiz",
        "choice",
        "created",
    )
    # list_filter = ("source",)
    ordering = ("id",)
    actions = [
        "export_as_csv",
        "export_as_json",
        "export_as_yaml",
        # "export_all_questionanswerevent_as_yaml",
    ]

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in obj._meta.fields]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class DailyStatAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "date",
        "question_answer_count",
        # "quiz_answer_count",
        "question_feedback_count",
        # "quiz_feedback_count",
        "created",
    )
    list_filter = ("date",)
    ordering = ("id",)
    actions = ["export_as_csv", "export_as_json", "export_as_yaml"]

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in obj._meta.fields]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        """
        show chart of answers per day
        https://dev.to/danihodovic/integrating-chart-js-with-django-admin-1kjb

        Corresponding template in templates/admin/api/dailystat/change_list.html
        """
        if request.POST.get("run_generate_daily_stats_script", False):
            management.call_command("generate_daily_stats")

        # custom form
        current_field = str(
            request.POST.get("field", constants.AGGREGATION_FIELD_CHOICE_LIST[0])
        )
        current_scale = str(
            request.POST.get("scale", constants.AGGREGATION_SCALE_CHOICE_LIST[0])
        )

        # Aggregate answers per day
        # chart_data_query = DailyStat.objects.extra(select={"day": "date(date)"}) # sqlite
        chart_data_query = DailyStat.objects.agg_timeseries(
            current_field, scale=current_scale
        )

        chart_data_list = list(chart_data_query)

        # get answers since today ?
        # no, need to run script to populate the values
        daily_stat_last = DailyStat.objects.last()
        daily_stat_last_date = (
            daily_stat_last.date if daily_stat_last else datetime(1970, 1, 1)
        )

        # Serialize and attach the chart data to the template context
        chart_data_json = json.dumps(chart_data_list, cls=DjangoJSONEncoder)
        extra_context = extra_context or {
            "chart_data": chart_data_json,
            "daily_stat_last_date": daily_stat_last_date,
            "field_choice_list": constants.AGGREGATION_FIELD_CHOICE_LIST,
            "current_field": current_field,
            "scale_choice_list": constants.AGGREGATION_SCALE_CHOICE_LIST,
            "current_scale": current_scale,
        }

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


class ContributionAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "text",
        "type",
        "created",
    )
    readonly_fields = (
        "text",
        "description",
    )

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


class LogEntryAdmin(admin.ModelAdmin):
    """
    https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#logentry-objects
    """

    list_display = (
        "object_repr",
        "content_type",
        "action_flag",
        "user",
        "action_time",
    )
    list_filter = (
        "content_type",
        "user",
    )
    ordering = ("-action_time",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class MyAdminSite(AdminSite):
    site_header = "Know Your Planet administration"
    enable_nav_sidebar = False
    index_template = "admin/index_with_export.html"

    def index(self, request, extra_context=None):
        """
        Corresponding template in templates/admin/api/index_with_export.html
        """

        export_message = ""

        if request.POST.get("run_export_data_to_github_script", False):
            out = StringIO()
            request.POST.get("run_export_data_to_github_script")
            management.call_command("export_data_to_github", stdout=out)
            if "https" not in out.getvalue():
                export_message = f"Erreur survenue. {out.getvalue()}"
            else:
                export_message = f"La Pull Request a été créé !<br>Elle est visible ici : <a href='{out.getvalue()}' target='_blank'>{out.getvalue()}</a>"  # noqa
            print(export_message)

        extra_context = extra_context or {"export_message": export_message}

        # Call the superclass index to render the page
        return super().index(request, extra_context=extra_context)


admin_site = MyAdminSite(name="myadmin")

admin_site.register(Question, QuestionAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Tag, TagAdmin)
admin_site.register(Quiz, QuizAdmin)
admin_site.register(QuestionAnswerEvent, QuestionAnswerEventAdmin)
admin_site.register(QuestionFeedbackEvent, QuestionFeedbackEventAdmin)
admin_site.register(QuestionAggStat, QuestionAggStatAdmin)
admin_site.register(QuizAnswerEvent, QuizAnswerEventAdmin)
admin_site.register(QuizFeedbackEvent, QuizFeedbackEventAdmin)
admin_site.register(DailyStat, DailyStatAdmin)
admin_site.register(Contribution, ContributionAdmin)
admin_site.register(Glossary, GlossaryAdmin)
admin_site.register(admin.models.LogEntry, LogEntryAdmin)
