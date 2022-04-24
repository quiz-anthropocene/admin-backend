from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, SingleTableView

from api.tags.serializers import TagSerializer
from questions.models import Question
from quizs.models import Quiz
from tags.filters import TagFilter
from tags.forms import TagEditForm
from tags.models import Tag
from tags.tables import TagTable


class TagListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Tag
    template_name = "tags/list.html"
    context_object_name = "tags"
    table_class = TagTable
    filterset_class = TagFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("questions", "quizs")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_params = [value for (key, value) in self.request.GET.items() if ((key not in ["page"]) and value)]
        if len(request_params):
            context["active_filters"] = True
        return context


class TagDetailView(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = "tags/detail_view.html"
    context_object_name = "tag"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.get_object()
        context["tag_dict"] = TagSerializer(tag).data
        return context


class TagDetailEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = TagEditForm
    template_name = "tags/detail_edit.html"
    success_message = "Le tag a été mis à jour."
    # success_url = reverse_lazy("tags:detail_view")

    def get_object(self):
        return get_object_or_404(Tag, id=self.kwargs.get("pk"))

    def get_success_url(self):
        return reverse_lazy("tags:detail_view", args=[self.kwargs.get("pk")])


class TagDetailQuestionsView(LoginRequiredMixin, SingleTableView):
    model = Question
    template_name = "tags/detail_questions.html"
    context_object_name = "questions"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("category").prefetch_related("tags")
        qs = qs.filter(tags__in=[self.kwargs.get("pk")])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = Tag.objects.get(id=self.kwargs.get("pk"))
        return context


class TagDetailQuizsView(LoginRequiredMixin, SingleTableView):
    model = Quiz
    template_name = "tags/detail_quizs.html"
    context_object_name = "quizs"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("tags")
        qs = qs.filter(tags__in=[self.kwargs.get("pk")])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = Tag.objects.get(id=self.kwargs.get("pk"))
        return context
