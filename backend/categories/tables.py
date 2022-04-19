import django_tables2 as tables

from categories.models import Category


class CategoryTable(tables.Table):
    id = tables.Column(linkify=lambda record: record.get_absolute_url())

    class Meta:
        model = Category
        template_name = "django_tables2/bootstrap4.html"
        attrs = {"class": "table-responsive table-striped table-bordered border-primary font-size-small"}
