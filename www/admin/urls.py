from django.urls import include, path

from www.admin.views import AdminContributorCreateView, AdminContributorListView, AdminHistoryListView, AdminHomeView


app_name = "admin"

urlpatterns = [
    path("", AdminHomeView.as_view(), name="home"),
    path(
        "contributors/",
        include(
            [
                path("", AdminContributorListView.as_view(), name="contributor_list"),
                path("create/", AdminContributorCreateView.as_view(), name="contributor_create"),
            ]
        ),
    ),
    path("history/", AdminHistoryListView.as_view(), name="history"),
]
