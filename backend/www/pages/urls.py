from django.urls import path
from django.views.generic import TemplateView

from www.pages.views import HomeView


app_name = "pages"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("403/", TemplateView.as_view(template_name="403.html"), name="403"),
]
