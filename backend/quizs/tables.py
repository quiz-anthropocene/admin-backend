import django_tables2 as tables
from django.utils.html import format_html

from core.tables import ChoiceColumn, ImageColumn, RichTextEllipsisColumn
from quizs.models import Quiz


QUIZ_FIELD_SEQUENCE = [field.name for field in Quiz._meta.fields + Quiz._meta.model._meta.many_to_many]
QUIZ_FIELD_SEQUENCE.remove("questions")  # not displayed
QUIZ_FIELD_SEQUENCE.remove("relationships")  # not displayed
QUIZ_FIELD_SEQUENCE.remove("tags")  # change position
QUIZ_FIELD_SEQUENCE.insert(QUIZ_FIELD_SEQUENCE.index("difficulty_average"), "tags")


class QuizTable(tables.Table):
    id = tables.Column(linkify=lambda record: record.get_absolute_url())
    introduction = RichTextEllipsisColumn(attrs={"td": {"title": lambda record: record.introduction}})
    conclusion = RichTextEllipsisColumn(attrs={"td": {"title": lambda record: record.conclusion}})
    # questions
    tags = tables.ManyToManyColumn(
        transform=lambda tag: format_html(
            f'<a href="{tag.get_absolute_url()}"><span class="badge bg-primary">{tag.name}</span></a>'
        ),
        separator=" ",
    )
    image_background_url = ImageColumn()
    # relationships

    class Meta:
        model = Quiz
        sequence = QUIZ_FIELD_SEQUENCE
        template_name = "django_tables2/bootstrap4.html"
        attrs = {"class": "table-responsive table-striped table-bordered border-primary font-size-small"}

    def __init__(self, *args, **kwargs):
        for field_name in Quiz.QUIZ_CHOICE_FIELDS + Quiz.QUIZ_FK_FIELDS:  # + Quiz.QUIZ_LIST_FIELDS:
            self.base_columns[field_name] = ChoiceColumn()
        for field_name in Quiz.QUIZ_BOOLEAN_FIELDS:
            self.base_columns[field_name] = tables.BooleanColumn(yesno="✅,❌")
        super(QuizTable, self).__init__(*args, **kwargs)
