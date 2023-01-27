import json
from datetime import datetime

from django.contrib import admin
from django.core import management
from django.core.serializers.json import DjangoJSONEncoder

from contributions.models import Contribution
from core.admin import ExportMixin, admin_site
from core.models import Configuration
from stats import constants
from stats.models import (
    DailyStat,
    LinkClickEvent,
    QuestionAggStat,
    QuestionAnswerEvent,
    QuestionFeedbackEvent,
    QuizAggStat,
    QuizAnswerEvent,
    QuizFeedbackEvent,
)


class QuestionAggStatAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "question_id",
        "answer_count",
        "answer_success_count",
        "like_count",
        "dislike_count",
    )
    actions = [
        "export_as_csv",
    ]

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in obj._meta.fields]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class QuestionAnswerEventAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "question",
        "choice",
        "source",
        "created",
    )
    list_filter = ("source",)
    ordering = ("-id",)
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

        Corresponding template in templates/admin/stats/questionanswerevent/change_list.html
        """
        # Aggregate answers per day
        chart_data_query = QuestionAnswerEvent.objects.agg_timeseries()

        chart_data_list = list(chart_data_query)

        # get answers since today
        if len(chart_data_list) and (str(chart_data_list[-1]["day"]) != str(datetime.now().date())):
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
    ordering = ("-id",)
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


class QuizAggStatAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "quiz_id",
        "answer_count",
        "like_count",
        "dislike_count",
    )
    actions = [
        "export_as_csv",
    ]

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
        "duration_seconds",
        "created",
    )
    list_filter = ("quiz",)
    ordering = ("-id",)
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

        Corresponding template in templates/admin/stats/quizanswerevent/change_list.html
        """
        # Aggregate answers per day
        # chart_data_query = QuizAnswerEvent.objects.extra(select={"day": "date(created)"}) # sqlite
        chart_data_query = QuizAnswerEvent.objects.agg_timeseries()

        chart_data_list = list(chart_data_query)

        # get answers since today
        if len(chart_data_list) and (str(chart_data_list[-1]["day"]) != str(datetime.now().date())):
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
    ordering = ("-id",)
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


class LinkClickEventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "quiz",
        "question",
        "link_url",
        "created",
    )
    # list_filter = ("quiz",)
    ordering = ("-id",)

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
        "quiz_answer_count",
        "question_feedback_count",
        # "quiz_feedback_count",
        "created",
    )
    list_filter = ("date",)
    ordering = ("-id",)
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

        Corresponding template in templates/admin/stats/dailystat/change_list.html
        """
        if request.POST.get("run_generate_daily_stats_script", False):
            management.call_command("generate_daily_stats")

        # custom form
        current_field = str(request.POST.get("field", constants.AGGREGATION_FIELD_CHOICE_LIST[0]))
        current_scale = str(request.POST.get("scale", constants.AGGREGATION_SCALE_CHOICE_LIST[0]))
        current_since_date = str(request.POST.get("since_date", constants.AGGREGATION_SINCE_DATE_DEFAULT))

        # Aggregate answers per day
        # chart_data_query = DailyStat.objects.extra(select={"day": "date(date)"}) # sqlite
        chart_data_query = DailyStat.objects.agg_timeseries(
            current_field, scale=current_scale, since_date=current_since_date
        )

        chart_data_list = list(chart_data_query)

        # Serialize and attach the chart data to the template context
        chart_data_json = json.dumps(chart_data_list, cls=DjangoJSONEncoder)
        extra_context = extra_context or {
            "configuration": Configuration.get_solo(),
            "chart_data": chart_data_json,
            "field_choice_list": constants.AGGREGATION_FIELD_CHOICE_LIST,
            "current_field": current_field,
            "scale_choice_list": constants.AGGREGATION_SCALE_CHOICE_LIST,
            "current_scale": current_scale,
            "question_answer_count": DailyStat.objects.agg_count("question_answer_count"),
            "question_public_answer_count": DailyStat.objects.agg_count("question_public_answer_count"),
            "question_answer_count_last_30_days": DailyStat.objects.agg_count(
                "question_answer_count", since="last_30_days"
            ),
            "question_public_answer_count_last_30_days": DailyStat.objects.agg_count(
                "question_public_answer_count", since="last_30_days"
            ),
            "quiz_answer_count": DailyStat.objects.agg_count("quiz_answer_count"),
            "quiz_public_answer_count": DailyStat.objects.agg_count("quiz_public_answer_count"),
            "quiz_answer_count_last_30_days": DailyStat.objects.agg_count("quiz_answer_count", since="last_30_days"),
            "quiz_public_answer_count_last_30_days": DailyStat.objects.agg_count(
                "quiz_public_answer_count", since="last_30_days"
            ),
            "question_feedback_count": DailyStat.objects.agg_count("question_feedback_count"),
            "question_feedback_count_last_30_days": DailyStat.objects.agg_count(
                "question_feedback_count", since="last_30_days"
            ),
            "quiz_feedback_count": DailyStat.objects.agg_count("quiz_feedback_count"),
            "quiz_feedback_count_last_30_days": DailyStat.objects.agg_count(
                "quiz_feedback_count", since="last_30_days"
            ),
            "contribution_count": Contribution.objects.exclude(type="erreur application").count(),
            "contribution_count_last_30_days": Contribution.objects.exclude(type="erreur application")
            .last_30_days()
            .count(),
            "since_date_min": constants.AGGREGATION_SINCE_DATE_DEFAULT,
            "current_since_date": current_since_date,
        }

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


admin_site.register(QuestionAggStat, QuestionAggStatAdmin)
admin_site.register(QuestionAnswerEvent, QuestionAnswerEventAdmin)
admin_site.register(QuestionFeedbackEvent, QuestionFeedbackEventAdmin)
admin_site.register(QuizAggStat, QuizAggStatAdmin)
admin_site.register(QuizAnswerEvent, QuizAnswerEventAdmin)
admin_site.register(QuizFeedbackEvent, QuizFeedbackEventAdmin)
admin_site.register(LinkClickEvent, LinkClickEventAdmin)
admin_site.register(DailyStat, DailyStatAdmin)
