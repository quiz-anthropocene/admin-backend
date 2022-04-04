from django.contrib.auth import views as auth_views
from django.urls import path

from www.auth.views import LoginView


app_name = "auth"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="auth/logged_out.html"), name="logout"),
]
