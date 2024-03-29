from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


"""
UserPassesTestMixin cannot be stacked
https://docs.djangoproject.com/en/4.0/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin.get_test_func
https://stackoverflow.com/a/60302594/4293684

How to have LoginRequiredMixin (redirects to next url if anonymous) + custom mixin ?
--> custom dispatch() method
"""


class LoginRequiredUserPassesTestMixin(UserPassesTestMixin):
    """
    Custom mixin that mimicks the LoginRequiredMixin behavior
    https://stackoverflow.com/a/59661739
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        return super().dispatch(request, *args, **kwargs)


class ContributorUserRequiredMixin(LoginRequiredUserPassesTestMixin):
    """
    Restrict access to users with (at least) Contributor role
    """

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.has_role_contributor

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("pages:home"))


class SuperContributorUserRequiredMixin(LoginRequiredUserPassesTestMixin):
    """
    Restrict access to users with (at least) Super-Contributor role
    """

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.has_role_super_contributor

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("profile:home"))


class AdministratorUserRequiredMixin(LoginRequiredUserPassesTestMixin):
    """
    Restrict access to users with Administrator role
    """

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.has_role_administrator

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("profile:home"))
