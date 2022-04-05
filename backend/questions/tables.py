import django_tables2 as tables
from django.utils.html import format_html

from core.tables import ChoiceColumn, ImageColumn, LongTextEllipsisColumn
from questions.models import Question


class QuestionTable(tables.Table):
    id = tables.Column(linkify=lambda record: record.get_absolute_url())
    text = LongTextEllipsisColumn(attrs={"td": {"title": lambda record: record.text}})
    type = ChoiceColumn()
    category = ChoiceColumn()
    tags = tables.ManyToManyColumn(
        transform=lambda tag: format_html(f'<span class="badge bg-primary">{tag.name}</span>'), separator=" "
    )
    difficulty = ChoiceColumn()
    language = ChoiceColumn()
    answer_correct = ChoiceColumn()
    has_ordered_answers = tables.BooleanColumn(yesno="✅,❌")
    answer_explanation = LongTextEllipsisColumn(attrs={"td": {"title": lambda record: record.answer_explanation}})
    answer_image_explanation = LongTextEllipsisColumn(
        attrs={"td": {"title": lambda record: record.answer_image_explanation}}
    )
    answer_extra_info = LongTextEllipsisColumn(attrs={"td": {"title": lambda record: record.answer_extra_info}})
    answer_image_url = ImageColumn()
    validation_status = ChoiceColumn()
    author = ChoiceColumn()
    validator = ChoiceColumn()

    class Meta:
        model = Question
        template_name = "django_tables2/bootstrap4.html"
        # fields = ("id", "category", "tags")
        attrs = {"class": "table-responsive table-striped table-bordered border-primary font-size-small"}
