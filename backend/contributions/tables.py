import django_tables2 as tables

from contributions.models import Question
from core.tables import ChoiceColumn


class ContributionTable(tables.Table):
    type = ChoiceColumn()
    # text = LongTextEllipsisColumn(attrs={"td": {"title": lambda record: record.text}})
    question = tables.Column(
        verbose_name="Question", accessor="question.id", attrs={"td": {"title": lambda record: record.question}}
    )
    quiz = tables.Column(verbose_name="Quiz", accessor="quiz.id", attrs={"td": {"title": lambda record: record.quiz}})

    class Meta:
        model = Question
        template_name = "django_tables2/bootstrap4.html"
        fields = ["type", "text", "question", "quiz", "created"]  # description
        attrs = {"class": "table-responsive table-striped table-bordered border-primary font-size-small"}
