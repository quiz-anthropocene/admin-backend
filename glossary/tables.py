import django_tables2 as tables

from core.tables import RichTextEllipsisColumn
from glossary.models import GlossaryItem


class GlossaryTable(tables.Table):
    id = tables.Column(linkify=lambda record: record.get_absolute_url())
    description = RichTextEllipsisColumn(attrs={"td": {"title": lambda record: record.description}})

    class Meta:
        model = GlossaryItem
        template_name = "django_tables2/bootstrap4.html"
        attrs = {"class": "table-responsive table-striped table-bordered border-primary font-size-small"}
