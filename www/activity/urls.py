from django.urls import path

from www.activity.views import EventListView


app_name = "activity"

urlpatterns = [
    path("", EventListView.as_view(), name="list"),
]
