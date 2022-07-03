import django_filters

from core import constants
from users import constants as user_constants
from users.models import User


class ContributorFilter(django_filters.FilterSet):
    roles = django_filters.ChoiceFilter(
        label="Rôle", choices=user_constants.USER_ROLE_CHOICES, lookup_expr="icontains"
    )
    has_question = django_filters.ChoiceFilter(
        label="Auteur de questions ?", choices=constants.BOOLEAN_CHOICES, method="has_question_filter"
    )
    has_quiz = django_filters.ChoiceFilter(
        label="Auteur de quizs ?", choices=constants.BOOLEAN_CHOICES, method="has_quiz_filter"
    )

    class Meta:
        model = User
        fields = ["roles", "has_question", "has_quiz"]

    def has_question_filter(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.has_question()

    def has_quiz_filter(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.has_quiz()
