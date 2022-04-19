import django_tables2 as tables
from django.utils.html import format_html

from core.tables import ChoiceColumn, ImageColumn, LongTextEllipsisColumn
from questions.models import Question


class QuestionTable(tables.Table):
    id = tables.Column(linkify=lambda record: record.get_absolute_url())
    text = LongTextEllipsisColumn(attrs={"td": {"title": lambda record: record.text}})
    tags = tables.ManyToManyColumn(
        transform=lambda tag: format_html(
            f'<a href="{tag.get_absolute_url()}"><span class="badge bg-primary">{tag.name}</span></a>'
        ),
        separator=" ",
    )
    answer_explanation = LongTextEllipsisColumn(attrs={"td": {"title": lambda record: record.answer_explanation}})
    answer_image_explanation = LongTextEllipsisColumn(
        attrs={"td": {"title": lambda record: record.answer_image_explanation}}
    )
    answer_extra_info = LongTextEllipsisColumn(attrs={"td": {"title": lambda record: record.answer_extra_info}})
    answer_image_url = ImageColumn()

    class Meta:
        model = Question
        template_name = "django_tables2/bootstrap4.html"
        # fields = ("id", "category", "tags")
        attrs = {"class": "table-responsive table-striped table-bordered border-primary font-size-small"}

    def __init__(self, *args, **kwargs):
        for field_name in Question.QUESTION_CHOICE_FIELDS + Question.QUESTION_FK_FIELDS:
            self.base_columns[field_name] = ChoiceColumn()
        for field_name in Question.QUESTION_BOOLEAN_FIELDS:
            self.base_columns[field_name] = tables.BooleanColumn(yesno="✅,❌")
        super(QuestionTable, self).__init__(*args, **kwargs)
