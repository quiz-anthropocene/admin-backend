import django_filters
from django import forms
from django.forms import NumberInput

from core import constants
from quizs.models import Quiz
from tags.models import Tag


class QuizFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(widget=NumberInput(attrs={"min": 0}))
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())
    publish = django_filters.ChoiceFilter(choices=constants.BOOLEAN_CHOICES)
    has_audio = django_filters.ChoiceFilter(choices=constants.BOOLEAN_CHOICES)
    q = django_filters.CharFilter(
        label="Recherche",
        method="text_search",
        widget=forms.TextInput(attrs={"placeholder": "Dans les champs 'nom', 'introduction' et 'conclusion'"}),
    )

    class Meta:
        model = Quiz
        fields = ["id", "tags", "language", "has_audio", "author", "validation_status", "publish", "visibility", "q"]

    def text_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.simple_search(value)
