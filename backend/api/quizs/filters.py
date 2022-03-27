import django_filters

from core import constants
from tags.models import Tag


class QuizFilter(django_filters.FilterSet):
    language = django_filters.MultipleChoiceFilter(label="Langue(s) du quiz", choices=constants.LANGUAGE_CHOICES)
    tags = django_filters.ModelMultipleChoiceFilter(
        label="Tag(s)",
        queryset=Tag.objects.all(),
    )
    author = django_filters.CharFilter(label="Auteur du quiz")
    # TODO: QuizFullSerializer, QuizWithQuestionOrderSerializer
