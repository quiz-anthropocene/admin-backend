from django.views.generic import TemplateView
from django_tables2.views import SingleTableView

from core.mixins import ContributorUserRequiredMixin
from users.models import User
from users.tables import AdministratorTable


class UserHomeView(ContributorUserRequiredMixin, TemplateView):
    template_name = "users/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contributor_count"] = User.objects.all_contributors().count()
        context["quiz_author_count"] = User.objects.has_public_quiz().count()
        context["administrator_count"] = User.objects.all_administrators().count()
        return context


class AdministratorListView(ContributorUserRequiredMixin, SingleTableView):
    model = User
    template_name = "users/administrator_list.html"
    context_object_name = "administrators"
    table_class = AdministratorTable

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.all_administrators()
        qs = qs.order_by("created")
        return qs
