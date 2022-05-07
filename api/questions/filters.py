import django_filters

from categories.models import Category
from core import constants
from tags.models import Tag
from users.models import User


class QuestionFilter(django_filters.FilterSet):
    type = django_filters.MultipleChoiceFilter(label="Type(s) de question", choices=constants.QUESTION_TYPE_CHOICES)
    difficulty = django_filters.MultipleChoiceFilter(
        label="Niveau(x) de difficulté de la question",
        choices=constants.QUESTION_DIFFICULTY_CHOICES,
    )
    language = django_filters.MultipleChoiceFilter(label="Langue(s)", choices=constants.LANGUAGE_CHOICES)
    category = django_filters.ModelMultipleChoiceFilter(
        label="Catégorie(s)",
        queryset=Category.objects.all(),
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        label="Tag(s)",
        queryset=Tag.objects.all(),
    )
    author = django_filters.ModelMultipleChoiceFilter(
        label="Auteur(s)",
        queryset=User.objects.all_contributors(),
    )
    # TODO: QuestionFullStringSerializer, random
