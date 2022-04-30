from django import forms

from quizs.models import Quiz
from quizs.tables import QUIZ_FIELD_SEQUENCE
from tags.models import Tag


QUIZ_FORM_FIELDS = [field_name for field_name in QUIZ_FIELD_SEQUENCE if field_name not in Quiz.QUIZ_READONLY_FIELDS]


class QuizEditForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = QUIZ_FORM_FIELDS
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].queryset = Tag.objects.all().order_by("name")
