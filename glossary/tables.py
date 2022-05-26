import django_tables2 as tables

from core.tables import DEFAULT_ATTRS, DEFAULT_TEMPLATE, RichTextEllipsisColumn
from glossary.models import GlossaryItem


class GlossaryTable(tables.Table):
    id = tables.Column(linkify=lambda record: record.get_absolute_url())
    description = RichTextEllipsisColumn(attrs={"td": {"title": lambda record: record.description}})

    class Meta:
        model = GlossaryItem
        template_name = DEFAULT_TEMPLATE
        attrs = DEFAULT_ATTRS
