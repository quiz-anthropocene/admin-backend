import django_tables2 as tables
from django.utils.html import format_html

from core.tables import ChoiceColumn, ImageColumn, LongTextEllipsisColumn
from quizs.models import Quiz


class QuizTable(tables.Table):
    introduction = LongTextEllipsisColumn(attrs={"td": {"title": lambda record: record.introduction}})
    conclusion = LongTextEllipsisColumn(attrs={"td": {"title": lambda record: record.conclusion}})
    tags = tables.ManyToManyColumn(
        transform=lambda tag: format_html(f'<span class="badge bg-primary">{tag.name}</span>'), separator=" "
    )
    language = ChoiceColumn()
    author = ChoiceColumn()
    image_background_url = ImageColumn()
    has_audio = tables.BooleanColumn(yesno="✅,❌")
    publish = tables.BooleanColumn(yesno="✅,❌")
    spotlight = tables.BooleanColumn(yesno="✅,❌")

    class Meta:
        model = Quiz
        template_name = "django_tables2/bootstrap4.html"
        # fields = ("id", "category", "tags")
        attrs = {"class": "table-responsive table-striped table-bordered border-primary font-size-small"}
