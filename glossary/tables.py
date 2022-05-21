import django_tables2 as tables

from glossary.models import GlossaryItem


class GlossaryTable(tables.Table):
    class Meta:
        model = GlossaryItem
        template_name = "django_tables2/bootstrap4.html"
        attrs = {"class": "table-responsive table-striped table-bordered border-primary font-size-small"}
