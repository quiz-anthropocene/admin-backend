from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from contributions.filters import ContributionFilter
from contributions.models import Contribution
from contributions.tables import ContributionTable


class ContributionListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Contribution
    template_name = "contributions/list.html"
    context_object_name = "contributions"
    table_class = ContributionTable
    filterset_class = ContributionFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.exclude_errors().order_by("-created")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_params = [value for (key, value) in self.request.GET.items() if ((key not in ["page"]) and value)]
        if len(request_params):
            context["active_filters"] = True
        return context
