import django_filters

from contributions.models import Comment


class CommentFilter(django_filters.FilterSet):
    class Meta:
        model = Comment
        fields = ["type", "status"]
