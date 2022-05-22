import django_filters
from django.forms import NumberInput

from questions.models import Question
from tags.models import Tag


class QuestionFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(widget=NumberInput(attrs={"min": 0}))
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())

    class Meta:
        model = Question
        fields = [
            "id",
            "type",
            "category",
            "tags",
            "difficulty",
            "language",
            "author",
            "validation_status",
            "visibility",
        ]
