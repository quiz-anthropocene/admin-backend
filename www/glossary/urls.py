from django.urls import path

from www.glossary.views import GlossaryItemCreateView, GlossaryListView


app_name = "glossary"

urlpatterns = [
    path("", GlossaryListView.as_view(), name="list"),
    path("create/", GlossaryItemCreateView.as_view(), name="create"),
]
