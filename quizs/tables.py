import django_tables2 as tables
from django.utils.html import format_html

from core.tables import DEFAULT_ATTRS, DEFAULT_TEMPLATE, ChoiceColumn, ImageColumn, RichTextEllipsisColumn
from questions.models import Question
from quizs.models import Quiz, QuizQuestion


QUIZ_FIELD_SEQUENCE = [
    field.name
    for field in (Quiz._meta.fields + Quiz._meta.model._meta.many_to_many)
    if field.name not in Quiz.QUIZ_FLATTEN_FIELDS
]
QUIZ_FIELD_SEQUENCE.remove("questions")  # not displayed
QUIZ_FIELD_SEQUENCE.remove("relationships")  # not displayed
QUIZ_FIELD_SEQUENCE.remove("tags")  # change position
QUIZ_FIELD_SEQUENCE.remove("authors")  # change position
QUIZ_FIELD_SEQUENCE.insert(QUIZ_FIELD_SEQUENCE.index("difficulty_average"), "tags")
QUIZ_FIELD_SEQUENCE.insert(QUIZ_FIELD_SEQUENCE.index("image_background_url"), "authors")


class QuizTable(tables.Table):
    id = tables.Column(linkify=lambda record: record.get_absolute_url())
    introduction = RichTextEllipsisColumn(attrs={"td": {"title": lambda record: record.introduction}})
    conclusion = RichTextEllipsisColumn(attrs={"td": {"title": lambda record: record.conclusion}})
    authors = tables.ManyToManyColumn(
        transform=lambda author: format_html(f'<span class="badge bg-primary">{author.full_name}</span></a>')
        if author
        else "",
        separator=" ",
    )
    tags = tables.ManyToManyColumn(
        transform=lambda tag: format_html(
            f'<a href="{tag.get_absolute_url()}"><span class="badge bg-primary">{tag.name}</span></a>'
        ),
        separator=" ",
    )
    image_background_url = ImageColumn()
    # questions
    # relationships

    class Meta:
        model = Quiz
        fields = QUIZ_FIELD_SEQUENCE
        sequence = QUIZ_FIELD_SEQUENCE
        template_name = DEFAULT_TEMPLATE
        attrs = DEFAULT_ATTRS

    def __init__(self, *args, **kwargs):
        for field_name in Quiz.QUIZ_CHOICE_FIELDS + Quiz.QUIZ_FK_FIELDS:  # + Quiz.QUIZ_LIST_FIELDS:
            self.base_columns[field_name] = ChoiceColumn()
        for field_name in Quiz.QUIZ_BOOLEAN_FIELDS:
            self.base_columns[field_name] = tables.BooleanColumn(yesno="✅,❌")
        for field_name in Quiz.QUIZ_TIMESTAMP_FIELDS:
            self.base_columns[field_name] = tables.DateTimeColumn(format="d F Y")
        super().__init__(*args, **kwargs)


QUIZ_QUESTION_FIELD_SEQUENCE = [
    "question_id",
    "question_text",
    "question_type",
    "question_author",
    "question_validation_status",
    "question_visibility",
    "order",
]


class QuizQuestionTable(tables.Table):
    question_id = tables.Column(
        verbose_name=Question._meta.verbose_name,
        accessor="question.id",
        linkify=lambda record: record.question.get_absolute_url(),
    )
    question_text = RichTextEllipsisColumn(
        accessor="question.text", attrs={"td": {"title": lambda record: record.question.text}}
    )
    question_type = ChoiceColumn(verbose_name=Question._meta.get_field("type").verbose_name, accessor="question.type")
    question_author = ChoiceColumn(
        verbose_name=Question._meta.get_field("author").verbose_name, accessor="question.author"
    )
    question_validation_status = ChoiceColumn(
        verbose_name=Question._meta.get_field("validation_status").verbose_name, accessor="question.validation_status"
    )
    question_visibility = ChoiceColumn(
        verbose_name=Question._meta.get_field("visibility").verbose_name, accessor="question.visibility"
    )

    class Meta:
        model = QuizQuestion
        fields = QUIZ_QUESTION_FIELD_SEQUENCE
        sequence = QUIZ_QUESTION_FIELD_SEQUENCE
        template_name = DEFAULT_TEMPLATE
        attrs = DEFAULT_ATTRS
