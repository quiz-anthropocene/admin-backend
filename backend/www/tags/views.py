from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django_tables2.views import SingleTableView

from api.tags.serializers import TagSerializer
from questions.models import Question
from tags.models import Tag
from tags.tables import TagTable


class TagListView(LoginRequiredMixin, SingleTableView):
    model = Tag
    template_name = "tags/list.html"
    context_object_name = "tags"
    table_class = TagTable


class TagDetailView(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = "tags/detail_view.html"
    context_object_name = "tag"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.get_object()
        context["tag_dict"] = TagSerializer(tag).data
        return context


class TagDetailQuestionsView(LoginRequiredMixin, SingleTableView):
    model = Question
    template_name = "tags/detail_questions.html"
    context_object_name = "questions"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("tags")
        qs = qs.filter(tags__in=[self.kwargs.get("pk")])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = Tag.objects.get(id=self.kwargs.get("pk"))
        return context
