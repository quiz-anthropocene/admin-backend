from django.urls import path

from www.users.views import AdministratorListView, UserHomeView


app_name = "users"

urlpatterns = [
    path("", UserHomeView.as_view(), name="home"),
    path("administrators/", AdministratorListView.as_view(), name="administrator_list"),
]
