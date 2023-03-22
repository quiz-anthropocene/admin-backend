from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, UpdateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from api.glossary.serializers import GlossaryItemSerializer
from core.forms import form_filters_cleaned_dict, form_filters_to_list
from core.mixins import ContributorUserRequiredMixin
from glossary.filters import GlossaryItemFilter
from glossary.forms import GLOSSARY_ITEM_FORM_FIELDS, GlossaryItemCreateForm, GlossaryItemEditForm
from glossary.models import GlossaryItem
from glossary.tables import GlossaryTable
from history.utilities import get_diff_between_two_history_records


class GlossaryListView(ContributorUserRequiredMixin, SingleTableMixin, FilterView):
    model = GlossaryItem
    template_name = "glossary/list.html"
    context_object_name = "glossary"
    table_class = GlossaryTable
    filterset_class = GlossaryItemFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context["filter"].form.is_valid():
            search_dict = form_filters_cleaned_dict(context["filter"].form.cleaned_data)
            if search_dict:
                context["search_filters"] = form_filters_to_list(search_dict, with_delete_url=True)
        return context


class GlossaryItemDetailView(ContributorUserRequiredMixin, DetailView):
    model = GlossaryItem
    template_name = "glossary/detail_view.html"
    context_object_name = "glossary_item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        glossary_item = self.get_object()
        context["glossary_item_dict"] = GlossaryItemSerializer(glossary_item).data
        return context


class GlossaryItemDetailEditView(ContributorUserRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = GlossaryItemEditForm
    template_name = "glossary/detail_edit.html"
    context_object_name = "glossary_item"
    success_message = _("The glossary item was updated.")
    # success_url = reverse_lazy("glossary:detail_view")

    def get_object(self):
        return get_object_or_404(GlossaryItem, id=self.kwargs.get("pk"))

    def get_success_url(self):
        return reverse_lazy("glossary:detail_view", args=[self.kwargs.get("pk")])


class GlossaryItemDetailHistoryView(ContributorUserRequiredMixin, DetailView):
    model = GlossaryItem
    template_name = "glossary/detail_history.html"
    context_object_name = "glossary_item"

    def get_object(self):
        return get_object_or_404(GlossaryItem, id=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["glossary_item_history"] = self.get_object().history.all()
        context["glossary_item_history_delta"] = list()
        for record in context["glossary_item_history"]:
            new_record = record
            if new_record.prev_record:
                delta_changes = get_diff_between_two_history_records(
                    new_record, old_record=new_record.prev_record, returns="changes"
                )
                context["glossary_item_history_delta"].append(delta_changes)
            else:
                # probably a create action
                # we create the diff ourselves because there isn't any previous record
                delta_fields = GLOSSARY_ITEM_FORM_FIELDS
                delta_new = [{"field": k, "new": v} for k, v in record.__dict__.items() if k in delta_fields if v]
                context["glossary_item_history_delta"].append(delta_new)
        return context


class GlossaryItemCreateView(ContributorUserRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = GlossaryItemCreateForm
    template_name = "glossary/create.html"
    success_url = reverse_lazy("glossary:list")
    # success_message = ""

    def get_success_message(self, cleaned_data):
        return mark_safe(
            _("The glossary item <strong>{glossary_item_name}</strong> was created.").format(
                glossary_item_name=self.object.name
            )
        )
