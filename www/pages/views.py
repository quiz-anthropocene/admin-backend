from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django_tables2.views import SingleTableView

from activity.models import Event
from core.mixins import ContributorUserRequiredMixin
from users.models import User
from users.tables import AdministratorTable


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("auth:login"))
        if request.user.is_authenticated and not request.user.has_role_contributor:
            return HttpResponseRedirect(reverse_lazy("pages:403"))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_10_events"] = Event.objects.display().order_by("-created")[:10]
        return context


class HelpView(ContributorUserRequiredMixin, TemplateView):
    template_name = "pages/help.html"


class AdministratorListView(ContributorUserRequiredMixin, SingleTableView):
    model = User
    template_name = "pages/administrator_list.html"
    context_object_name = "administrators"
    table_class = AdministratorTable

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.all_administrators()
        qs = qs.order_by("created")
        return qs
