import django_filters
from django import forms
from django.forms import NumberInput
from django.utils.translation import gettext_lazy as _

from questions.models import Question
from tags.models import Tag


TEXT_SEARCH_PLACEHOLDER = (
    f"{_('In the following fields:')} "
    f"{Question._meta.get_field('text').verbose_name}, "
    f"{_('Answer choices')}, "
    f"{Question._meta.get_field('answer_explanation').verbose_name}"
)


class QuestionFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(widget=NumberInput(attrs={"min": 0}))
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())
    q = django_filters.CharFilter(
        label=_("Text search"),
        method="text_search",
        widget=forms.TextInput(attrs={"placeholder": TEXT_SEARCH_PLACEHOLDER}),
    )

    class Meta:
        model = Question
        fields = [
            "id",
            "type",
            "category",
            "tags",
            "difficulty",
            "language",
            "author",
            "validation_status",
            "visibility",
            "q",
        ]

    def text_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.simple_search(value)
