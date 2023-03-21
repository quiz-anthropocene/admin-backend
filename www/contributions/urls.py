from django.urls import include, path
from django.views.generic.base import RedirectView

from www.contributions.views import (
    CommentDetailEditView,
    CommentDetailHistoryView,
    CommentDetailReplyCreateView,
    CommentDetailView,
    CommentListView,
)


app_name = "contributions"

urlpatterns = [
    path("", CommentListView.as_view(), name="list"),
    path(
        "<int:pk>/",
        include(
            [
                # path("", CommentDetailView.as_view(), name="detail"),
                path(
                    "",
                    RedirectView.as_view(pattern_name="contributions:detail_view", permanent=False),
                    name="detail",
                ),
                path("view/", CommentDetailView.as_view(), name="detail_view"),
                path("edit/", CommentDetailEditView.as_view(), name="detail_edit"),
                path("reply/", CommentDetailReplyCreateView.as_view(), name="detail_reply_create"),
                path("history/", CommentDetailHistoryView.as_view(), name="detail_history"),
            ]
        ),
    ),
]
