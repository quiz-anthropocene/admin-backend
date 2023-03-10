from django.views.generic import TemplateView

from core.mixins import ContributorUserRequiredMixin
from users.models import User


class UserHomeView(ContributorUserRequiredMixin, TemplateView):
    template_name = "users/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contributor_count"] = User.objects.all_contributors().count()
        context["quiz_author_count"] = User.objects.has_public_quiz().count()
        context["administrator_count"] = User.objects.all_administrators().count()
        return context
