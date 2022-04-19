import django_tables2 as tables

from core.tables import LongTextEllipsisColumn
from tags.models import Tag


class TagTable(tables.Table):
    id = tables.Column(linkify=lambda record: record.get_absolute_url())
    description = LongTextEllipsisColumn(attrs={"td": {"title": lambda record: record.description}})

    class Meta:
        model = Tag
        template_name = "django_tables2/bootstrap4.html"
        attrs = {"class": "table-responsive table-striped table-bordered border-primary font-size-small"}
