from django.urls import path

from www.admin.views import AdminContributorListView, AdminHistoryListView, AdminHomeView


app_name = "admin"

urlpatterns = [
    path("", AdminHomeView.as_view(), name="home"),
    path("contributors/", AdminContributorListView.as_view(), name="contributors"),
    path("history/", AdminHistoryListView.as_view(), name="history"),
]
