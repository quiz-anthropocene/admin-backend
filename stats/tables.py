import django_tables2 as tables
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_tables2.utils import Accessor

from core.tables import DEFAULT_ATTRS, DEFAULT_TEMPLATE, RichTextEllipsisColumn
from questions.models import Question
from quizs.models import Quiz
from stats.models import QuestionAggStat, QuizAggStat


QUESTION_FIELD_SEQUENCE = [field.name for field in QuestionAggStat._meta.fields]
QUESTION_FIELD_SEQUENCE.insert(QUESTION_FIELD_SEQUENCE.index("question"), "question_id")
# QUESTION_FIELD_SEQUENCE.insert(QUESTION_FIELD_SEQUENCE.index("answer_count"), "question_id")
# QUESTION_FIELD_SEQUENCE.insert(QUESTION_FIELD_SEQUENCE.index("answer_count"), "question_text")
QUESTION_FIELD_SEQUENCE.insert(QUESTION_FIELD_SEQUENCE.index("like_count"), "success_rate")

QUIZ_FIELD_SEQUENCE = [field.name for field in QuizAggStat._meta.fields]
QUIZ_FIELD_SEQUENCE.insert(QUIZ_FIELD_SEQUENCE.index("quiz"), "quiz_id")
QUIZ_FIELD_SEQUENCE.insert(QUIZ_FIELD_SEQUENCE.index("like_count"), "success_rate")


class QuestionStatsTable(tables.Table):
    question_id = tables.Column(
        verbose_name=_("ID"),
        accessor=Accessor("question.id"),
        linkify=lambda record: reverse("questions:detail_stats", kwargs={"pk": record.question.id}),
    )
    question = RichTextEllipsisColumn(
        verbose_name=Question._meta.get_field("text").verbose_name, accessor=Accessor("question.text")
    )
    success_rate = tables.Column(
        verbose_name=_("Successfully answered"), empty_values=(), order_by=("answer_success_count", "answer_count")
    )

    class Meta:
        model = QuestionAggStat
        fields = QUESTION_FIELD_SEQUENCE
        sequence = QUESTION_FIELD_SEQUENCE
        template_name = DEFAULT_TEMPLATE
        attrs = DEFAULT_ATTRS

    def render_success_rate(self, value, record):
        return record.question.success_rate


class QuizStatsTable(tables.Table):
    quiz_id = tables.Column(
        verbose_name=_("ID"),
        accessor=Accessor("quiz.id"),
        linkify=lambda record: reverse("quizs:detail_stats", kwargs={"pk": record.quiz.id}),
    )
    quiz = RichTextEllipsisColumn(
        verbose_name=Quiz._meta.get_field("name").verbose_name, accessor=Accessor("quiz.name")
    )
    success_rate = tables.Column(
        verbose_name=_("Successfully answered"),
        empty_values=(),
        order_by=("-quiz__stats__answer_success_count", "quiz__stats__question_count"),
    )

    class Meta:
        model = QuizAggStat
        fields = QUIZ_FIELD_SEQUENCE
        sequence = QUIZ_FIELD_SEQUENCE
        template_name = DEFAULT_TEMPLATE
        attrs = DEFAULT_ATTRS

    def render_success_rate(self, record):
        return record.quiz.success_rate
