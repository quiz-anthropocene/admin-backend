from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, DetailView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from api.glossary.serializers import GlossaryItemSerializer
from core.mixins import ContributorUserRequiredMixin
from glossary.forms import GlossaryItemCreateForm
from glossary.models import GlossaryItem
from glossary.tables import GlossaryTable


class GlossaryListView(ContributorUserRequiredMixin, SingleTableMixin, FilterView):
    model = GlossaryItem
    template_name = "glossary/list.html"
    context_object_name = "glossary"
    table_class = GlossaryTable


class GlossaryItemDetailView(ContributorUserRequiredMixin, DetailView):
    model = GlossaryItem
    template_name = "glossary/detail_view.html"
    context_object_name = "glossaryitem"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        glossaryitem = self.get_object()
        context["glossaryitem_dict"] = GlossaryItemSerializer(glossaryitem).data
        return context


class GlossaryItemCreateView(ContributorUserRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = GlossaryItemCreateForm
    template_name = "glossary/create.html"
    success_url = reverse_lazy("glossary:list")
    # success_message = ""

    def get_success_message(self, cleaned_data):
        return mark_safe(f"Le terme <strong>{self.object.name}</strong> a été crée avec succès.")
