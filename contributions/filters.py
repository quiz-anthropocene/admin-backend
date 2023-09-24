import django_filters

from contributions.models import Comment
from core import constants


class CommentFilter(django_filters.FilterSet):
    publish = django_filters.ChoiceFilter(choices=constants.BOOLEAN_CHOICES)

    class Meta:
        model = Comment
        fields = ["type", "status", "publish"]


class CommentNewFilter(django_filters.FilterSet):
    class Meta:
        model = Comment
        fields = ["type"]
