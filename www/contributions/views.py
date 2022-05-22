from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from api.contributions.serializers import ContributionSerializer
from contributions.filters import ContributionFilter
from contributions.forms import ContributionStatusEditForm
from contributions.models import Contribution
from contributions.tables import ContributionTable
from core.mixins import ContributorUserRequiredMixin


class ContributionListView(ContributorUserRequiredMixin, SingleTableMixin, FilterView):
    model = Contribution
    template_name = "contributions/list.html"
    context_object_name = "contributions"
    table_class = ContributionTable
    filterset_class = ContributionFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.exclude_errors().exclude_answers().order_by("-created")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_params = [value for (key, value) in self.request.GET.items() if ((key not in ["page"]) and value)]
        if len(request_params):
            context["active_filters"] = True
        return context


class ContributionDetailView(ContributorUserRequiredMixin, DetailView):
    model = Contribution
    template_name = "contributions/detail_view.html"
    context_object_name = "contribution"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contribution = self.get_object()
        context["contribution_dict"] = ContributionSerializer(contribution).data
        return context


class ContributionDetailEditView(ContributorUserRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = ContributionStatusEditForm
    template_name = "contributions/detail_edit.html"
    context_object_name = "contribution"
    success_message = "La contribution a été mise à jour."
    # success_url = reverse_lazy("contributions:detail_view")

    def get_object(self):
        return get_object_or_404(Contribution, id=self.kwargs.get("pk"))

    def get_success_url(self):
        return reverse_lazy("contributions:detail_view", args=[self.kwargs.get("pk")])
