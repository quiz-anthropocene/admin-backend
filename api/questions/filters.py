import django_filters
from django.utils.translation import gettext_lazy as _

from categories.models import Category
from core import constants
from tags.models import Tag
from users.models import User


class QuestionFilter(django_filters.FilterSet):
    type = django_filters.MultipleChoiceFilter(label=_("Type(s)"), choices=constants.QUESTION_TYPE_CHOICES)
    difficulty = django_filters.MultipleChoiceFilter(
        label=_("Difficulty level(s)"),
        choices=constants.QUESTION_DIFFICULTY_CHOICES,
    )
    language = django_filters.MultipleChoiceFilter(label=_("Language(s)"), choices=constants.LANGUAGE_CHOICES)
    category = django_filters.ModelMultipleChoiceFilter(
        label=_("Category(s)"),
        queryset=Category.objects.all(),
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        label=_("Tag(s)"),
        queryset=Tag.objects.all(),
    )
    author = django_filters.ModelMultipleChoiceFilter(
        label=_("Author(s)"),
        queryset=User.objects.all_contributors(),
    )
    # TODO: QuestionFullStringSerializer, random
