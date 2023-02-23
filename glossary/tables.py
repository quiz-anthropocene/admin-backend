import django_tables2 as tables

from core.tables import DEFAULT_ATTRS, DEFAULT_TEMPLATE, ChoiceColumn, RichTextEllipsisColumn
from glossary.models import GlossaryItem


class GlossaryTable(tables.Table):
    id = tables.Column(linkify=lambda record: record.get_absolute_url())
    description = RichTextEllipsisColumn(attrs={"td": {"title": lambda record: record.description}})

    class Meta:
        model = GlossaryItem
        template_name = DEFAULT_TEMPLATE
        attrs = DEFAULT_ATTRS

    def __init__(self, *args, **kwargs):
        for field_name in GlossaryItem.GLOSSARY_ITEM_CHOICE_FIELDS:
            self.base_columns[field_name] = ChoiceColumn()
        super().__init__(*args, **kwargs)
