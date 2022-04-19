from django.urls import include, path
from django.views.generic.base import RedirectView

from www.tags.views import TagDetailQuestionsView, TagDetailView, TagListView


app_name = "tags"

urlpatterns = [
    path("", TagListView.as_view(), name="list"),
    # path("<int:pk>/", TagDetailView.as_view(), name="detail"),
    path(
        "<int:pk>/",
        include(
            [
                # path("", TagDetailView.as_view(), name="detail"),
                path(
                    "",
                    RedirectView.as_view(pattern_name="tags:detail_view", permanent=False),
                    name="detail",
                ),
                path("view/", TagDetailView.as_view(), name="detail_view"),
                path("questions/", TagDetailQuestionsView.as_view(), name="detail_questions"),
            ]
        ),
    ),
]
