import django_tables2 as tables

from contributions.models import Contribution
from core.tables import ChoiceColumn, RichTextLongerEllipsisColumn


class ContributionTable(tables.Table):
    type = ChoiceColumn()
    text = RichTextLongerEllipsisColumn(attrs={"td": {"title": lambda record: record.text}})
    question = tables.Column(
        verbose_name="Question",
        accessor="question.id",
        linkify=lambda record: record.question.get_absolute_url(),
        attrs={"td": {"title": lambda record: record.question}},
    )
    quiz = tables.Column(
        verbose_name="Quiz",
        accessor="quiz.id",
        linkify=lambda record: record.quiz.get_absolute_url(),
        attrs={"td": {"title": lambda record: record.quiz}},
    )
    processed = tables.Column(verbose_name="Traité", accessor="processed")
    # has_replies = tables.BooleanColumn(verbose_name="Répondu", yesno="✅,❌")
    action = tables.TemplateColumn(
        verbose_name="Actions",
        template_name="contributions/_table_action_items.html",
        attrs={"th": {"style": "min-width:130px"}},
    )

    class Meta:
        model = Contribution
        template_name = "django_tables2/bootstrap4.html"
        fields = ["type", "text", "question", "quiz", "status", "created"]  # id, description
        attrs = {"class": "table-responsive table-striped table-bordered border-primary font-size-small"}
