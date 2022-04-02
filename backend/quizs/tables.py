import django_tables2 as tables

from quizs.models import Quiz


class QuizTable(tables.Table):
    tags = tables.ManyToManyColumn(transform=lambda tag: tag.name)

    class Meta:
        model = Quiz
        template_name = "django_tables2/bootstrap4.html"
        # fields = ("id", "category", "tags")
        attrs = {"class": "table-striped table-bordered border-primary"}
