import django_filters

from questions.models import Question
from tags.models import Tag


class QuestionFilter(django_filters.FilterSet):
    # type = django_filters.ChoiceFilter(
    #     label="Type", choices=constants.QUESTION_TYPE_CHOICES
    # )  # empty_label="--- Type ---"
    # category = django_filters.ModelChoiceFilter(label="Category", queryset=Category.objects.all())
    tags = django_filters.ModelMultipleChoiceFilter(label="Tag", queryset=Tag.objects.all())
    # difficulty = django_filters.ChoiceFilter(label="Difficulty", choices=constants.QUESTION_DIFFICULTY_CHOICES)
    # language = django_filters.ChoiceFilter(label="Language", choices=constants.LANGUAGE_CHOICES)
    # validation_status = django_filters.ChoiceFilter(
    #     label="Validation status", choices=constants.QUESTION_VALIDATION_STATUS_CHOICES
    # )

    class Meta:
        model = Question
        fields = ["type", "category", "tags", "difficulty", "language", "author", "validation_status"]
