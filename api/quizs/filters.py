import django_filters

from core import constants
from tags.models import Tag
from users.models import User


class QuizFilter(django_filters.FilterSet):
    language = django_filters.MultipleChoiceFilter(label="Langue(s)", choices=constants.LANGUAGE_CHOICES)
    tags = django_filters.ModelMultipleChoiceFilter(
        label="Tag(s)",
        queryset=Tag.objects.all(),
    )
    authors = django_filters.ModelMultipleChoiceFilter(
        label="Auteur(s)",
        queryset=User.objects.all_contributors(),
    )
    # TODO: QuizFullSerializer, QuizWithQuestionOrderSerializer
