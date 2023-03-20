from django.urls import path

from www.users.views import AdministratorListView, AuthorCardList, UserHomeView


app_name = "users"

urlpatterns = [
    path("", UserHomeView.as_view(), name="home"),
    path("authors/", AuthorCardList.as_view(), name="author_card_list"),
    path("administrators/", AdministratorListView.as_view(), name="administrator_list"),
]
