import django_filters
from django import forms
from django.forms import NumberInput

from questions.models import Question
from tags.models import Tag


class QuestionFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(widget=NumberInput(attrs={"min": 0}))
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())
    q = django_filters.CharFilter(
        label="Recherche",
        method="text_search",
        widget=forms.TextInput(attrs={"placeholder": "Dans les champs 'texte', 'réponses' ou 'explication'"}),
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
