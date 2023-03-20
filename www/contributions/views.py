from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from api.contributions.serializers import CommentSerializer
from contributions.filters import CommentFilter
from contributions.forms import CommentReplyCreateForm, CommentStatusEditForm
from contributions.models import Comment
from contributions.tables import CommentTable
from core.forms import form_filters_cleaned_dict, form_filters_to_list
from core.mixins import ContributorUserRequiredMixin


class CommentListView(ContributorUserRequiredMixin, SingleTableMixin, FilterView):
    model = Comment
    template_name = "contributions/list.html"
    context_object_name = "contributions"
    table_class = CommentTable
    filterset_class = CommentFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("replies")
        qs = qs.exclude_errors().exclude_contributor_work()
        qs = qs.order_by("-created")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context["filter"].form.is_valid():
            search_dict = form_filters_cleaned_dict(context["filter"].form.cleaned_data)
            if search_dict:
                context["search_filters"] = form_filters_to_list(search_dict, with_delete_url=True)
        return context


class CommentDetailView(ContributorUserRequiredMixin, DetailView):
    model = Comment
    template_name = "contributions/detail_view.html"
    context_object_name = "contribution"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contribution = self.get_object()
        context["contribution_dict"] = CommentSerializer(contribution).data
        return context


class CommentDetailEditView(ContributorUserRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = CommentStatusEditForm
    template_name = "contributions/detail_edit.html"
    context_object_name = "contribution"
    success_message = "La contribution a été mise à jour."
    # success_url = reverse_lazy("contributions:detail_view")

    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs.get("pk"))

    def get(self, request, *args, **kwargs):
        contribution = self.get_object()
        if contribution and contribution.parent:
            return redirect(reverse_lazy("contributions:detail_view", args=[contribution.parent.id]))
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("contributions:detail_view", args=[self.kwargs.get("pk")])


class CommentDetailReplyCreateView(ContributorUserRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CommentReplyCreateForm
    template_name = "contributions/detail_reply_create.html"
    success_message = "Votre message a été ajouté."
    # success_url = reverse_lazy("contributions:detail_view")

    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs.get("pk"))

    def get(self, request, *args, **kwargs):
        contribution = self.get_object()
        if contribution and contribution.parent:
            return redirect(reverse_lazy("contributions:detail_view", args=[contribution.parent.id]))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contribution = self.get_object()
        context["contribution"] = contribution
        context["contribution_replies"] = contribution.replies.all()
        return context

    def get_initial(self):
        return {"author": self.request.user, "parent": self.get_object()}

    def get_success_url(self):
        return reverse_lazy("contributions:detail_view", args=[self.kwargs.get("pk")])
