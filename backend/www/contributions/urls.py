from django.urls import path

from www.contributions.views import ContributionListView


app_name = "contributions"

urlpatterns = [
    path("", ContributionListView.as_view(), name="list"),
]
