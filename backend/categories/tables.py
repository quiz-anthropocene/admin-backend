import django_tables2 as tables
from django.db.models import Count

from categories.models import Category
from core.tables import RichTextColumn


CATEGORY_FIELD_SEQUENCE = [field.name for field in Category._meta.fields]
CATEGORY_FIELD_SEQUENCE.insert(CATEGORY_FIELD_SEQUENCE.index("created"), "question_count")


class CategoryTable(tables.Table):
    id = tables.Column(linkify=lambda record: record.get_absolute_url())
    description = RichTextColumn(attrs={"td": {"title": lambda record: record.description}})
    question_count = tables.Column(verbose_name="Questions")

    class Meta:
        model = Category
        sequence = CATEGORY_FIELD_SEQUENCE
        template_name = "django_tables2/bootstrap4.html"
        attrs = {"class": "table-responsive table-striped table-bordered border-primary font-size-small"}

    def __init__(self, *args, **kwargs):
        for field_name in Category.CATEGORY_TIMESTAMP_FIELDS:
            self.base_columns[field_name] = tables.DateTimeColumn(format="d F Y")
        super(CategoryTable, self).__init__(*args, **kwargs)

    def order_question_count(self, queryset, is_descending):
        queryset = queryset.annotate(question_agg=Count("questions")).order_by(
            ("-" if is_descending else "") + "question_agg"
        )
        return (queryset, True)
