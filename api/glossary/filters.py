import django_filters
from django.utils.translation import gettext_lazy as _

from core import constants


class GlossaryItemFilter(django_filters.FilterSet):
    language = django_filters.MultipleChoiceFilter(label=_("Language(s)"), choices=constants.LANGUAGE_CHOICES)
