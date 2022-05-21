from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from core.mixins import ContributorUserRequiredMixin
from glossary.models import GlossaryItem
from glossary.tables import GlossaryTable


class GlossaryListView(ContributorUserRequiredMixin, SingleTableMixin, FilterView):
    model = GlossaryItem
    template_name = "glossary/list.html"
    context_object_name = "glossary"
    table_class = GlossaryTable
