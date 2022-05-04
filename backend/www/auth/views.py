from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from www.auth.forms import LoginForm, PasswordResetForm


class LoginView(auth_views.LoginView):
    template_name = "auth/login.html"
    form_class = LoginForm
    redirect_authenticated_user = True
    # success_url = settings.LOGIN_REDIRECT_URL


class PasswordResetView(auth_views.PasswordResetView):
    template_name = "auth/password_reset.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("auth:password_reset_sent")  # see get_success_url() below
    email_template_name = "auth/password_reset_email_body.html"
    subject_template_name = "auth/password_reset_email_subject.txt"

    def get_success_url(self):
        success_url = super().get_success_url()
        user_email = self.request.POST.get("email")
        return f"{success_url}?email={user_email}"
