import django_filters
from django import forms
from django.forms import NumberInput
from django.utils.translation import gettext_lazy as _

from core import constants
from quizs.models import Quiz
from tags.models import Tag


TEXT_SEARCH_PLACEHOLDER = (
    f"{_('In the following fields:')} "
    f"{Quiz._meta.get_field('name').verbose_name}, "
    f"{Quiz._meta.get_field('introduction').verbose_name}, "
    f"{Quiz._meta.get_field('conclusion').verbose_name}"
)


class QuizFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(widget=NumberInput(attrs={"min": 0}))
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())
    publish = django_filters.ChoiceFilter(choices=constants.BOOLEAN_CHOICES)
    has_audio = django_filters.ChoiceFilter(choices=constants.BOOLEAN_CHOICES)
    q = django_filters.CharFilter(
        label=_("Text search"),
        method="text_search",
        widget=forms.TextInput(attrs={"placeholder": TEXT_SEARCH_PLACEHOLDER}),
    )

    class Meta:
        model = Quiz
        fields = ["id", "authors", "tags", "language", "has_audio", "validation_status", "publish", "visibility", "q"]

    def text_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.simple_search(value)
