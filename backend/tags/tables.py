import django_tables2 as tables
from django.db.models import Count

from core.tables import RichTextColumn
from tags.models import Tag


TAG_FIELD_SEQUENCE = [field.name for field in Tag._meta.fields]
TAG_FIELD_SEQUENCE.insert(TAG_FIELD_SEQUENCE.index("created"), "question_count")
TAG_FIELD_SEQUENCE.insert(TAG_FIELD_SEQUENCE.index("created"), "quiz_count")


class TagTable(tables.Table):
    id = tables.Column(linkify=lambda record: record.get_absolute_url())
    description = RichTextColumn(attrs={"td": {"title": lambda record: record.description}})
    question_count = tables.Column(verbose_name="Questions")
    quiz_count = tables.Column(verbose_name="Quizs")

    class Meta:
        model = Tag
        sequence = TAG_FIELD_SEQUENCE
        template_name = "django_tables2/bootstrap4.html"
        attrs = {"class": "table-responsive table-striped table-bordered border-primary font-size-small"}

    def order_question_count(self, queryset, is_descending):
        queryset = queryset.annotate(question_agg=Count("questions")).order_by(
            ("-" if is_descending else "") + "question_agg"
        )
        return (queryset, True)

    def order_quiz_count(self, queryset, is_descending):
        queryset = queryset.annotate(quiz_agg=Count("quizs")).order_by(("-" if is_descending else "") + "quiz_agg")
        return (queryset, True)
