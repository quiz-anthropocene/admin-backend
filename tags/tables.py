import django_tables2 as tables
from django.db.models import Count

from core.tables import DEFAULT_ATTRS, DEFAULT_TEMPLATE, RichTextColumn
from questions.models import Question
from quizs.models import Quiz
from tags.models import Tag


TAG_FIELD_SEQUENCE = [field.name for field in Tag._meta.fields]
TAG_FIELD_SEQUENCE.insert(TAG_FIELD_SEQUENCE.index("created"), "question_count")
TAG_FIELD_SEQUENCE.insert(TAG_FIELD_SEQUENCE.index("created"), "quiz_count")


class TagTable(tables.Table):
    id = tables.Column(linkify=lambda record: record.get_absolute_url())
    description = RichTextColumn(attrs={"td": {"title": lambda record: record.description}})
    question_count = tables.Column(verbose_name=Question._meta.verbose_name_plural)
    quiz_count = tables.Column(verbose_name=Quiz._meta.verbose_name_plural)

    class Meta:
        model = Tag
        fields = TAG_FIELD_SEQUENCE
        sequence = TAG_FIELD_SEQUENCE
        template_name = DEFAULT_TEMPLATE
        attrs = DEFAULT_ATTRS

    def __init__(self, *args, **kwargs):
        for field_name in Tag.TAG_TIMESTAMP_FIELDS:
            self.base_columns[field_name] = tables.DateTimeColumn(format="d F Y")
        super(TagTable, self).__init__(*args, **kwargs)

    def order_question_count(self, queryset, is_descending):
        queryset = queryset.annotate(question_agg=Count("questions")).order_by(
            ("-" if is_descending else "") + "question_agg"
        )
        return (queryset, True)

    def order_quiz_count(self, queryset, is_descending):
        queryset = queryset.annotate(quiz_agg=Count("quizs")).order_by(("-" if is_descending else "") + "quiz_agg")
        return (queryset, True)
