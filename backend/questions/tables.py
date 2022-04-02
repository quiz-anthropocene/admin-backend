import django_tables2 as tables

from questions.models import Question


class QuestionTable(tables.Table):
    tags = tables.ManyToManyColumn(transform=lambda tag: tag.name)

    class Meta:
        model = Question
        template_name = "django_tables2/bootstrap4.html"
        # fields = ("id", "category", "tags")
        attrs = {"class": "table-striped table-bordered border-primary"}
