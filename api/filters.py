import django_filters

from api import constants
from api.models import Tag
from categories.models import Category


class QuestionFilter(django_filters.FilterSet):
    type = django_filters.MultipleChoiceFilter(label="Type(s) de question", choices=constants.QUESTION_TYPE_CHOICES)
    difficulty = django_filters.MultipleChoiceFilter(
        label="Niveau(x) de difficulté de la question",
        choices=constants.QUESTION_DIFFICULTY_CHOICES,
    )
    language = django_filters.MultipleChoiceFilter(
        label="Langue(s) de la question", choices=constants.LANGUAGE_CHOICES
    )
    category = django_filters.ModelMultipleChoiceFilter(
        label="Catégorie(s)",
        queryset=Category.objects.all(),
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        label="Tag(s)",
        queryset=Tag.objects.all(),
    )
    author = django_filters.CharFilter(label="Auteur de la question")
    # TODO: QuestionFullStringSerializer, random


class QuizFilter(django_filters.FilterSet):
    language = django_filters.MultipleChoiceFilter(label="Langue(s) du quiz", choices=constants.LANGUAGE_CHOICES)
    tags = django_filters.ModelMultipleChoiceFilter(
        label="Tag(s)",
        queryset=Tag.objects.all(),
    )
    author = django_filters.CharFilter(label="Auteur du quiz")
    # TODO: QuizFullSerializer, QuizWithQuestionOrderSerializer
