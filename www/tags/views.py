from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, DetailView, UpdateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, SingleTableView

from api.tags.serializers import TagSerializer
from core.forms import form_filters_cleaned_dict, form_filters_to_list
from core.mixins import ContributorUserRequiredMixin
from questions.models import Question
from quizs.models import Quiz
from tags.filters import TagFilter
from tags.forms import TagCreateForm, TagEditForm
from tags.models import Tag
from tags.tables import TagTable


class TagListView(ContributorUserRequiredMixin, SingleTableMixin, FilterView):
    model = Tag
    template_name = "tags/list.html"
    context_object_name = "tags"
    table_class = TagTable
    filterset_class = TagFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("questions", "quizs")
        qs = qs.order_by("name")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context["filter"].form.is_valid():
            search_dict = form_filters_cleaned_dict(context["filter"].form.cleaned_data)
            if search_dict:
                context["search_filters"] = form_filters_to_list(search_dict, with_delete_url=True)
        return context


class TagDetailView(ContributorUserRequiredMixin, DetailView):
    model = Tag
    template_name = "tags/detail_view.html"
    context_object_name = "tag"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.get_object()
        context["tag_dict"] = TagSerializer(tag).data
        return context


class TagDetailEditView(ContributorUserRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = TagEditForm
    template_name = "tags/detail_edit.html"
    success_message = "Le tag a été mis à jour."
    # success_url = reverse_lazy("tags:detail_view")

    def get_object(self):
        return get_object_or_404(Tag, id=self.kwargs.get("pk"))

    def get_success_url(self):
        return reverse_lazy("tags:detail_view", args=[self.kwargs.get("pk")])


class TagDetailQuestionListView(ContributorUserRequiredMixin, SingleTableView):
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


class TagDetailQuizListView(ContributorUserRequiredMixin, SingleTableView):
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


class TagCreateView(ContributorUserRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TagCreateForm
    template_name = "tags/create.html"
    success_url = reverse_lazy("tags:list")

    def get_success_message(self, cleaned_data):
        return mark_safe(f"Le tag <strong>{cleaned_data['name']}</strong> a été crée avec succès.")
