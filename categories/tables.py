import django_tables2 as tables
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from categories.models import Category
from core.tables import DEFAULT_ATTRS, DEFAULT_TEMPLATE, RichTextColumn


CATEGORY_FIELD_SEQUENCE = [field.name for field in Category._meta.fields]
CATEGORY_FIELD_SEQUENCE.insert(CATEGORY_FIELD_SEQUENCE.index("created"), "question_count")


class CategoryTable(tables.Table):
    id = tables.Column(linkify=lambda record: record.get_absolute_url())
    description = RichTextColumn(attrs={"td": {"title": lambda record: record.description}})
    question_count = tables.Column(verbose_name=_("Questions"))

    class Meta:
        model = Category
        fields = CATEGORY_FIELD_SEQUENCE
        sequence = CATEGORY_FIELD_SEQUENCE
        template_name = DEFAULT_TEMPLATE
        attrs = DEFAULT_ATTRS

    def __init__(self, *args, **kwargs):
        for field_name in Category.CATEGORY_TIMESTAMP_FIELDS:
            self.base_columns[field_name] = tables.DateTimeColumn(format="d F Y")
        super(CategoryTable, self).__init__(*args, **kwargs)

    def order_question_count(self, queryset, is_descending):
        queryset = queryset.annotate(question_agg=Count("questions")).order_by(
            ("-" if is_descending else "") + "question_agg"
        )
        return (queryset, True)
