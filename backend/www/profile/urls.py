from django.urls import path
from django.views.generic.base import RedirectView

from www.profile.views import ProfileInfoView, ProfileQuestionsView, ProfileQuizsView


app_name = "profile"

urlpatterns = [
    path(
        "",
        RedirectView.as_view(pattern_name="profile:info", permanent=False),
        name="detail",
    ),
    path("info/", ProfileInfoView.as_view(), name="info"),
    path("questions/", ProfileQuestionsView.as_view(), name="questions"),
    path("quizs/", ProfileQuizsView.as_view(), name="quizs"),
]
