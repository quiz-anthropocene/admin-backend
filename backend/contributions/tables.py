import django_tables2 as tables

from contributions.models import Question
from core.tables import ChoiceColumn, LongTextEllipsisColumn


class ContributionTable(tables.Table):
    type = ChoiceColumn()
    text = LongTextEllipsisColumn(attrs={"td": {"title": lambda record: record.text}})
    # description

    class Meta:
        model = Question
        template_name = "django_tables2/bootstrap4.html"
        fields = ["type", "text", "question", "quiz", "created"]
        attrs = {"class": "table-responsive table-striped table-bordered border-primary font-size-small"}
