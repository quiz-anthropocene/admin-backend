from django.urls import path

from www.pages.views import HomeView


app_name = "pages"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
