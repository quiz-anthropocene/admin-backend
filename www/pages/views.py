from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.mixins import ContributorUserRequiredMixin


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("auth:login"))
        if request.user.is_authenticated and not request.user.has_role_contributor:
            return HttpResponseRedirect(reverse_lazy("pages:403"))
        return super().get(request, *args, **kwargs)


class HelpView(ContributorUserRequiredMixin, TemplateView):
    template_name = "pages/help.html"
