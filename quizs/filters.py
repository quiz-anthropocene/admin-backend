import django_filters
from django.forms import NumberInput

from core import constants
from quizs.models import Quiz
from tags.models import Tag


class QuizFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(widget=NumberInput(attrs={"min": 0}))
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())
    publish = django_filters.ChoiceFilter(choices=constants.BOOLEAN_CHOICES)
    has_audio = django_filters.ChoiceFilter(choices=constants.BOOLEAN_CHOICES)

    class Meta:
        model = Quiz
        fields = ["id", "tags", "language", "publish", "has_audio", "author", "visibility"]
