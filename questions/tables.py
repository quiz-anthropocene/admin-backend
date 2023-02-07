import django_tables2 as tables
from django.utils.html import format_html

from core.tables import DEFAULT_ATTRS, DEFAULT_TEMPLATE, ChoiceColumn, ImageColumn, RichTextEllipsisColumn
from questions.models import Question


QUESTION_FIELD_SEQUENCE = [
    field.name
    for field in (Question._meta.fields + Question._meta.model._meta.many_to_many)
    if field.name not in Question.QUESTION_FLATTEN_FIELDS
]
QUESTION_FIELD_SEQUENCE.remove("tags")  # change position
QUESTION_FIELD_SEQUENCE.insert(QUESTION_FIELD_SEQUENCE.index("difficulty"), "tags")


class QuestionTable(tables.Table):
    id = tables.Column(linkify=lambda record: record.get_absolute_url())
    text = RichTextEllipsisColumn(attrs={"td": {"title": lambda record: record.text}})
    tags = tables.ManyToManyColumn(
        transform=lambda tag: format_html(
            f'<a href="{tag.get_absolute_url()}"><span class="badge bg-primary">{tag.name}</span></a>'
        ),
        separator=" ",
    )
    answer_explanation = RichTextEllipsisColumn(attrs={"td": {"title": lambda record: record.answer_explanation}})
    answer_image_explanation = RichTextEllipsisColumn(
        attrs={"td": {"title": lambda record: record.answer_image_explanation}}
    )
    answer_extra_info = RichTextEllipsisColumn(attrs={"td": {"title": lambda record: record.answer_extra_info}})
    answer_image_url = ImageColumn()

    class Meta:
        model = Question
        fields = QUESTION_FIELD_SEQUENCE
        sequence = QUESTION_FIELD_SEQUENCE
        template_name = DEFAULT_TEMPLATE
        attrs = DEFAULT_ATTRS

    def __init__(self, *args, **kwargs):
        for field_name in Question.QUESTION_CHOICE_FIELDS + Question.QUESTION_FK_FIELDS:
            self.base_columns[field_name] = ChoiceColumn()
        for field_name in Question.QUESTION_BOOLEAN_FIELDS:
            self.base_columns[field_name] = tables.BooleanColumn(yesno="✅,❌")
        for field_name in Question.QUESTION_TIMESTAMP_FIELDS:
            self.base_columns[field_name] = tables.DateTimeColumn(format="d F Y")
            # attrs={"td": {"title": lambda record: getattr(record, field_name)}})
        super().__init__(*args, **kwargs)
