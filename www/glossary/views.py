from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from core.mixins import ContributorUserRequiredMixin
from glossary.forms import GlossaryItemCreateForm
from glossary.models import GlossaryItem
from glossary.tables import GlossaryTable


class GlossaryListView(ContributorUserRequiredMixin, SingleTableMixin, FilterView):
    model = GlossaryItem
    template_name = "glossary/list.html"
    context_object_name = "glossary"
    table_class = GlossaryTable


class GlossaryItemCreateView(ContributorUserRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = GlossaryItemCreateForm
    template_name = "glossary/create.html"
    success_url = reverse_lazy("glossary:list")
    # success_message = ""

    def get_success_message(self, cleaned_data):
        return mark_safe(f"Le terme <strong>{self.object.name}</strong> a été crée avec succès.")
