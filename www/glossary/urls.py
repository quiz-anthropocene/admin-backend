from django.urls import path

from www.glossary.views import GlossaryListView


app_name = "glossary"

urlpatterns = [
    path("", GlossaryListView.as_view(), name="list"),
]
