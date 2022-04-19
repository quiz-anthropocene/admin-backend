from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django_tables2.views import SingleTableView

from api.categories.serializers import CategorySerializer
from categories.models import Category
from categories.tables import CategoryTable
from questions.models import Question


class CategoryListView(LoginRequiredMixin, SingleTableView):
    model = Category
    template_name = "categories/list.html"
    context_object_name = "categories"
    table_class = CategoryTable


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = "categories/detail_view.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context["category_dict"] = CategorySerializer(category).data
        return context


class CategoryDetailQuestionsView(LoginRequiredMixin, SingleTableView):
    model = Question
    template_name = "categories/detail_questions.html"
    context_object_name = "questions"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("tags")
        qs = qs.filter(category_id=self.kwargs.get("pk"))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.get(id=self.kwargs.get("pk"))
        return context
