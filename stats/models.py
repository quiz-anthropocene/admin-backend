from datetime import date, timedelta

from django.db import models
from django.db.models import Count, Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core import constants as api_constants
from questions.models import Question
from quizs.models import Quiz
from stats import constants


class QuestionAggStat(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, primary_key=True, related_name="agg_stats")
    answer_count = models.PositiveIntegerField(default=0, help_text=_("Answers count"))
    answer_success_count = models.PositiveIntegerField(default=0, help_text=_("Right answers count"))
    like_count = models.PositiveIntegerField(default=0, help_text=_("Likes count"))
    dislike_count = models.PositiveIntegerField(default=0, help_text=_("Dislikes count"))


class QuestionAnswerEventQuerySet(models.QuerySet):
    def for_question(self, question_id):
        return self.filter(question=question_id)

    def from_quiz(self):
        return self.filter(source=constants.QUESTION_SOURCE_QUIZ)

    def agg_timeseries(self):
        queryset = self
        queryset = (
            queryset.extra(select={"day": "to_char(created, 'YYYY-MM-DD')"})
            .values("day")
            .annotate(y=Count("created"))
            .order_by("day")
        )
        return queryset


class QuestionAnswerEvent(models.Model):
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE, related_name="stats")
    choice = models.CharField(
        max_length=50,
        choices=api_constants.QUESTION_ANSWER_CHOICES,
        help_text=_("Answer chosen by the internet user"),
    )

    source = models.CharField(
        max_length=50,
        choices=constants.QUESTION_SOURCE_CHOICES,
        default=constants.QUESTION_SOURCE_QUESTION,
        help_text=_("Context in which the question was answered"),
    )
    quiz = models.ForeignKey(Quiz, related_name="question_stats", on_delete=models.CASCADE, null=True, blank=True)

    created = models.DateTimeField(default=timezone.now, help_text=_("Date & time of answer"))

    objects = QuestionAnswerEventQuerySet.as_manager()


class QuestionFeedbackEventQuerySet(models.QuerySet):
    def for_question(self, question_id):
        return self.filter(question=question_id)

    def liked(self):
        return self.filter(choice=constants.FEEDBACK_LIKE)

    def disliked(self):
        return self.filter(choice=constants.FEEDBACK_DISLIKE)

    def from_quiz(self):
        return self.filter(source=constants.QUESTION_SOURCE_QUIZ)


class QuestionFeedbackEvent(models.Model):
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE, related_name="feedbacks")
    choice = models.CharField(
        max_length=50,
        choices=constants.FEEDBACK_CHOICES,
        default=constants.FEEDBACK_LIKE,
        help_text=_("Opinion on the question"),
    )

    source = models.CharField(
        max_length=50,
        choices=constants.QUESTION_SOURCE_CHOICES,
        default=constants.QUESTION_SOURCE_QUESTION,
        help_text=_("the context in which the opinion was sent"),
    )
    quiz = models.ForeignKey(Quiz, related_name="question_feedbacks", on_delete=models.CASCADE, null=True, blank=True)

    created = models.DateTimeField(default=timezone.now, help_text=_("Date & time of the opinion"))

    objects = QuestionFeedbackEventQuerySet.as_manager()


class QuizAggStat(models.Model):
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE, primary_key=True, related_name="agg_stats")
    answer_count = models.PositiveIntegerField(default=0, help_text=_("Answers count"))
    like_count = models.PositiveIntegerField(default=0, help_text=_("Likes count"))
    dislike_count = models.PositiveIntegerField(default=0, help_text=_("Dislikes count"))
    # answer_success_count_split = models.JSONField(help_text="Les statistiques par nombre de réponses correctes")


class QuizAnswerEventQuerySet(models.QuerySet):
    def for_quiz(self, quiz_id):
        return self.filter(quiz=quiz_id)

    def last_30_days(self):
        return self.filter(created__date__gte=(date.today() - timedelta(days=30)))

    def agg_timeseries(self, scale="day"):
        queryset = self
        # scale
        if scale in ["day", "week"]:
            queryset = (
                queryset.extra(select={"day": "to_char(created, 'YYYY-MM-DD')"})
                .values("day")
                .annotate(y=Count("created"))
                .order_by("day")
            )
            if scale == "week":
                from stats import utilities

                return utilities.aggregate_timeseries_by_week(queryset)

        if scale == "month":
            queryset = (
                queryset.extra(select={"day": "to_char(created, 'YYYY-MM-01')"})
                .values("day")
                .annotate(y=Count("created"))
                .order_by("day")
            )

        return queryset


class QuizAnswerEvent(models.Model):
    quiz = models.ForeignKey(Quiz, null=True, on_delete=models.CASCADE, related_name="stats")
    # Why do we store the value instead of retrieving quiz.question_count ?
    # Because the value can change (adding or removing questions from a quiz)
    question_count = models.IntegerField(
        default=0,
        help_text=_("Quiz questions count"),
    )
    answer_success_count = models.IntegerField(
        default=0,
        help_text=_("Right answers count"),
    )
    duration_seconds = models.IntegerField(
        default=0,
        help_text=_("Duration(in seconds) to complete the quiz"),
    )
    question_answer_split = models.JSONField(
        default=dict,
        help_text=_("Details per question"),
    )
    created = models.DateTimeField(default=timezone.now, help_text=_("Date and time of answer"))

    objects = QuizAnswerEventQuerySet.as_manager()


class QuizFeedbackEventQuerySet(models.QuerySet):
    def liked(self):
        return self.filter(choice=constants.FEEDBACK_LIKE)

    def disliked(self):
        return self.filter(choice=constants.FEEDBACK_DISLIKE)

    def for_quiz(self, quiz_id):
        return self.filter(quiz=quiz_id)

    def agg_timeseries(self, scale="day"):
        queryset = self
        # scale
        if scale in ["day", "week"]:
            queryset = (
                queryset.extra(select={"day": "to_char(created, 'YYYY-MM-DD')"})
                .values("day")
                .annotate(y=Count("created"))
                .order_by("day")
            )
            if scale == "week":
                from stats import utilities

                return utilities.aggregate_timeseries_by_week(queryset)

        if scale == "month":
            queryset = (
                queryset.extra(select={"day": "to_char(created, 'YYYY-MM-01')"})
                .values("day")
                .annotate(y=Count("created"))
                .order_by("day")
            )

        return queryset


class QuizFeedbackEvent(models.Model):
    quiz = models.ForeignKey(Quiz, null=True, on_delete=models.CASCADE, related_name="feedbacks")
    choice = models.CharField(
        max_length=50,
        choices=constants.FEEDBACK_CHOICES,
        default=constants.FEEDBACK_LIKE,
        help_text=_("Opinion left on the quiz"),
    )
    created = models.DateTimeField(default=timezone.now, help_text=_("Date & time of opinion"))

    objects = QuizFeedbackEventQuerySet.as_manager()


class LinkClickEvent(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="link_clicks", blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="link_clicks", blank=True, null=True)
    field_name = models.CharField(verbose_name=_("Field name"), max_length=50, blank=True)
    link_url = models.URLField(verbose_name=_("Clicked link"), max_length=500, blank=True)

    created = models.DateTimeField(default=timezone.now, help_text=_("Date & time of click"))


class DailyStatManager(models.Manager):
    def agg_count(
        self,
        field="question_answer_count",
        since="total",
        week_or_month_iso_number=None,
    ):
        queryset = self
        # since
        if since not in constants.AGGREGATION_SINCE_CHOICE_LIST:
            raise ValueError(f"DailyStat agg_count: must be one of {constants.AGGREGATION_SINCE_CHOICE_LIST}")
        if since == "last_30_days":
            queryset = queryset.filter(date__gte=(date.today() - timedelta(days=30)))
        if since == "month":
            queryset = queryset.filter(date__month=week_or_month_iso_number)
        elif since == "week":
            queryset = queryset.filter(date__week=week_or_month_iso_number)
        # field
        queryset = queryset.aggregate(Sum(field))[field + "__sum"]
        # returns None if aggregation is done on an empty queryset
        return queryset or 0

    def agg_timeseries(
        self,
        field="question_answer_count",
        scale=constants.AGGREGATION_SCALE_CHOICE_LIST[0],
        since_date=constants.AGGREGATION_SINCE_DATE_DEFAULT,
    ):
        """
        Output:
        [{'day': '2020-07-24', 'y': 1}, {'day': '2020-08-04', 'y': 13}]
        """
        queryset = self
        # since_date
        queryset = queryset.filter(date__gte=since_date)
        # scale
        if scale not in constants.AGGREGATION_SCALE_CHOICE_LIST:
            raise ValueError(
                f"DailyStat agg_timeseries: must be one of {constants.AGGREGATION_SCALE_CHOICE_LIST}"  # noqa
            )
        if scale in ["day", "week"]:
            queryset = (
                queryset.extra(select={"day": "to_char(date, 'YYYY-MM-DD')", "y": field})
                .values("day", "y")
                .order_by("day")
            )
            if scale == "week":
                from stats import utilities

                return utilities.aggregate_timeseries_by_week(queryset)

        if scale == "month":
            queryset = (
                queryset.extra(select={"day": "to_char(date, 'YYYY-MM-01')"})  # use Trunc ?
                .values("day")
                .annotate(y=Sum(field))
                .order_by("day")
            )

        return queryset


class DailyStat(models.Model):
    date = models.DateField(help_text=_("Date of statistics"))
    # answers
    question_answer_count = models.PositiveIntegerField(default=0, help_text=_("Answered questions count"))
    question_public_answer_count = models.PositiveIntegerField(
        default=0, help_text=_("Answered public questions count")
    )
    question_answer_from_quiz_count = models.PositiveIntegerField(
        default=0, help_text=_("Answered questions within quiz count")
    )
    quiz_answer_count = models.PositiveIntegerField(default=0, help_text=_("Answered quizzes count"))
    quiz_public_answer_count = models.PositiveIntegerField(default=0, help_text=_("Answered public quizzes count"))
    # feedbacks
    question_feedback_count = models.PositiveIntegerField(default=0, help_text=_("Question feedbacks count"))
    question_feedback_from_quiz_count = models.PositiveIntegerField(
        default=0, help_text=_("Question feedbacks within quizzes count")
    )
    quiz_feedback_count = models.PositiveIntegerField(default=0, help_text=_("Quiz feedbacks count"))
    hour_split = models.JSONField(
        default=constants.daily_stat_hour_split_jsonfield_default_value,
        help_text=_("Hourly statistics"),
    )

    created = models.DateTimeField(default=timezone.now, help_text=_("Date & time of daily statistics"))
    updated = models.DateField(auto_now=True)

    objects = DailyStatManager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["date"], name="stat_date_unique")]

    def __str__(self):
        return f"{self.date}"
