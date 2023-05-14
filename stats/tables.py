import django_tables2 as tables
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_tables2.utils import Accessor

from core.tables import DEFAULT_ATTRS, DEFAULT_TEMPLATE, RichTextEllipsisColumn
from stats.models import QuestionAggStat, QuizAggStat


QUESTION_FIELD_SEQUENCE = [field.name for field in QuestionAggStat._meta.fields]
QUESTION_FIELD_SEQUENCE.remove("question")  # split into id and text
QUESTION_FIELD_SEQUENCE.insert(QUESTION_FIELD_SEQUENCE.index("answer_count"), "question_id")
QUESTION_FIELD_SEQUENCE.insert(QUESTION_FIELD_SEQUENCE.index("answer_count"), "question_text")
QUESTION_FIELD_SEQUENCE.insert(QUESTION_FIELD_SEQUENCE.index("like_count"), "success_rate")

QUIZ_FIELD_SEQUENCE = [field.name for field in QuizAggStat._meta.fields]
QUIZ_FIELD_SEQUENCE.insert(QUIZ_FIELD_SEQUENCE.index("quiz"), "quiz_id")
QUIZ_FIELD_SEQUENCE.insert(QUIZ_FIELD_SEQUENCE.index("like_count"), "success_rate")


class QuestionsStatsTable(tables.Table):
    question_id = tables.Column(
        accessor=Accessor("question.id"),
        verbose_name="Question id",
        linkify=lambda record: reverse("questions:detail_stats", kwargs={"pk": record.question.id}),
    )
    question_text = RichTextEllipsisColumn(accessor=Accessor("question.text"), verbose_name=_("Question text"))
    success_rate = tables.Column(
        verbose_name="Success rate", empty_values=(), order_by=("answer_success_count", "answer_count")
    )

    class Meta:
        model = QuestionAggStat
        fields = QUESTION_FIELD_SEQUENCE
        sequence = QUESTION_FIELD_SEQUENCE
        template_name = DEFAULT_TEMPLATE
        attrs = DEFAULT_ATTRS

    def render_success_rate(self, value, record):
        return record.question.success_rate


class QuizsStatsTable(tables.Table):
    quiz_id = tables.Column(
        accessor=Accessor("quiz.id"),
        verbose_name="Quiz id",
        linkify=lambda record: reverse("questions:detail_stats", kwargs={"pk": record.quiz.id}),
    )
    # quiz = RichTextEllipsisColumn(verbose_name="Quiz name")
    success_rate = tables.Column(
        verbose_name="Success rate",
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
