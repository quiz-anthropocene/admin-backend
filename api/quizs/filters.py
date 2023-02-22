import django_filters
from django.utils.translation import gettext_lazy as _

from core import constants
from tags.models import Tag
from users.models import User


class QuizFilter(django_filters.FilterSet):
    language = django_filters.MultipleChoiceFilter(label=_("Language(s)"), choices=constants.LANGUAGE_CHOICES)
    tags = django_filters.ModelMultipleChoiceFilter(
        label=_("Tag(s)"),
        queryset=Tag.objects.all(),
    )
    authors = django_filters.ModelMultipleChoiceFilter(
        label=_("Author(s)"),
        queryset=User.objects.all_contributors(),
    )
    spotlight = django_filters.BooleanFilter()
    # TODO: QuizFullSerializer, QuizWithQuestionOrderSerializer
