from django import forms
from django.forms.models import inlineformset_factory

from quizs.models import Quiz, QuizQuestion
from quizs.tables import QUIZ_FIELD_SEQUENCE
from tags.models import Tag


QUIZ_FORM_FIELDS = [field_name for field_name in QUIZ_FIELD_SEQUENCE if field_name not in Quiz.QUIZ_READONLY_FIELDS]
QUIZ_CREATE_FORM_FIELDS = [field_name for field_name in QUIZ_FORM_FIELDS if field_name not in ["publish", "spotlight"]]


class QuizCreateForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = QUIZ_CREATE_FORM_FIELDS
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].queryset = Tag.objects.all().order_by("name")
        # self.fields["publish"].disabled = True
        # self.fields["spotlight"].disabled = True


class QuizEditForm(QuizCreateForm):
    class Meta:
        model = Quiz
        fields = QUIZ_FORM_FIELDS

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["publish"].disabled = False
    #     self.fields["spotlight"].disabled = False


class QuizQuestionEditForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ["order"]
        # fields = ["question", "order"]


QuizQuestionFormSet = inlineformset_factory(Quiz, QuizQuestion, form=QuizQuestionEditForm, extra=1, can_delete=True)
