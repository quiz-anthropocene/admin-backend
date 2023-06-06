import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from core.tables import DEFAULT_ATTRS, DEFAULT_TEMPLATE, ChoiceColumn, RichTextEllipsisColumn
from glossary.models import GlossaryItem


GLOSSARY_FIELDS = [
    "name",
    "name_alternatives",
    "definition_short",
    "description",
    "has_description_accessible_url",
    "language",
    "created",
    "action",
]  # id, description_accessible_url, updated


class GlossaryTable(tables.Table):
    description = RichTextEllipsisColumn(attrs={"td": {"title": lambda record: record.description}})
    has_description_accessible_url = tables.Column(
        verbose_name=GlossaryItem._meta.get_field("description_accessible_url").verbose_name,
        accessor="has_description_accessible_url_icon",
    )
    action = tables.TemplateColumn(
        verbose_name=_("Actions"),
        template_name="glossary/_table_action_items.html",
        attrs={"th": {"style": "min-width:130px"}},
    )

    class Meta:
        model = GlossaryItem
        template_name = DEFAULT_TEMPLATE
        fields = GLOSSARY_FIELDS
        attrs = DEFAULT_ATTRS

    def __init__(self, *args, **kwargs):
        for field_name in GlossaryItem.GLOSSARY_ITEM_CHOICE_FIELDS:
            self.base_columns[field_name] = ChoiceColumn()
        super().__init__(*args, **kwargs)
