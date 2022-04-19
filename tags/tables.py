import django_tables2 as tables

from tags.models import Tag


class TagTable(tables.Table):
    id = tables.Column(linkify=lambda record: record.get_absolute_url())

    class Meta:
        model = Tag
        template_name = "django_tables2/bootstrap4.html"
        # fields = ("id", "category", "tags")
        attrs = {"class": "table-responsive table-striped table-bordered border-primary font-size-small"}
