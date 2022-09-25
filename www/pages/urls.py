from django.urls import include, path
from django.views.generic import TemplateView

from www.pages.views import AdministratorListView, HelpView, HomeView


app_name = "pages"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("help/", HelpView.as_view(), name="help"),
    path(
        "help/",
        include(
            [
                path("", HelpView.as_view(), name="help_home"),
                path("administrators", AdministratorListView.as_view(), name="help_administrator_list"),
            ]
        ),
    ),
    path("403/", TemplateView.as_view(template_name="403.html"), name="403"),
    path("404/", TemplateView.as_view(template_name="404.html"), name="404"),
    path("500/", TemplateView.as_view(template_name="500.html"), name="500"),
]
