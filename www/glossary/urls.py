from django.urls import include, path
from django.views.generic.base import RedirectView

from www.glossary.views import GlossaryItemCreateView, GlossaryItemDetailView, GlossaryListView


app_name = "glossary"

urlpatterns = [
    path("", GlossaryListView.as_view(), name="list"),
    path(
        "<int:pk>/",
        include(
            [
                # path("", GlossaryItemDetailView.as_view(), name="detail"),
                path(
                    "",
                    RedirectView.as_view(pattern_name="glossary:detail_view", permanent=False),
                    name="detail",
                ),
                path("view/", GlossaryItemDetailView.as_view(), name="detail_view"),
            ]
        ),
    ),
    path("create/", GlossaryItemCreateView.as_view(), name="create"),
]
