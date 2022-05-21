import django_filters

from core import constants
from quizs.models import Quiz
from tags.models import Tag


class QuizFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(label="Id")
    tags = django_filters.ModelChoiceFilter(label="Tag", queryset=Tag.objects.all())  # ModelMultipleChoiceFilter
    # language = django_filters.ChoiceFilter(label="Language", choices=constants.LANGUAGE_CHOICES)
    publish = django_filters.ChoiceFilter(label="Publish", choices=constants.BOOLEAN_CHOICES)
    has_audio = django_filters.ChoiceFilter(label="Has audio", choices=constants.BOOLEAN_CHOICES)

    class Meta:
        model = Quiz
        fields = ["tags", "language", "publish", "has_audio", "author", "visibility", "id"]
