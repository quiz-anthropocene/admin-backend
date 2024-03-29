from dal import autocomplete
from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from questions.models import Question
from quizs.models import Quiz, QuizQuestion
from quizs.tables import QUIZ_FIELD_SEQUENCE
from tags.models import Tag


QUIZ_READONLY_FORM_FIELDS = ["validation_status"]
QUIZ_HIDDEN_FORM_FIELDS = ["image_background_url"]
QUIZ_M2M_SEPERATE_FORM_FIELDS = ["questions", "relationships"]
QUIZ_FORM_FIELDS = [
    field_name
    for field_name in QUIZ_FIELD_SEQUENCE
    if field_name not in (Quiz.QUIZ_READONLY_FIELDS + QUIZ_M2M_SEPERATE_FORM_FIELDS)
]
QUIZ_CREATE_FORM_FIELDS = [field_name for field_name in QUIZ_FORM_FIELDS if field_name not in ["publish", "spotlight"]]


class QuizCreateForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = QUIZ_CREATE_FORM_FIELDS + QUIZ_READONLY_FORM_FIELDS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].queryset = Tag.objects.all().order_by("name")
        self.fields["image_background_url"].label = _("Quiz background image")
        # disable some fields
        for field_name in QUIZ_READONLY_FORM_FIELDS:
            self.fields[field_name].disabled = True
        # hide some fields (defaults)
        for field_name in QUIZ_HIDDEN_FORM_FIELDS:
            self.fields[field_name].widget = forms.HiddenInput()


class QuizEditForm(QuizCreateForm):
    class Meta:
        model = Quiz
        fields = QUIZ_FORM_FIELDS + QUIZ_READONLY_FORM_FIELDS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["validation_status"].disabled = False


class QuizQuestionEditForm(forms.ModelForm):
    question = forms.ModelChoiceField(
        queryset=Question.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="questions:search", attrs={"data-placeholder": "Recherche par ID ou Texte"}
        ),
    )

    class Meta:
        model = QuizQuestion
        fields = ["question", "order"]


QuizQuestionFormSet = inlineformset_factory(Quiz, QuizQuestion, form=QuizQuestionEditForm, extra=0, can_delete=True)
