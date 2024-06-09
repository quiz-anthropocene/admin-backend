from django import forms
from django.utils.translation import gettext_lazy as _

from questions.models import Question
from questions.tables import QUESTION_FIELD_SEQUENCE
from tags.models import Tag


QUESTION_READONLY_FORM_FIELDS = []  # "validation_status"
QUESTION_HIDDEN_FORM_FIELDS = ["answer_image_url"]
QUESTION_REQUIRED_FORM_FIELDS = [
    "answer_choice_a",
    "answer_choice_b",
    "answer_correct",
    "author_certify_necessary_rights",
]
QUESTION_FORM_FIELDS = [
    field_name for field_name in QUESTION_FIELD_SEQUENCE if field_name not in Question.QUESTION_READONLY_FIELDS
]


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = QUESTION_FORM_FIELDS + QUESTION_READONLY_FORM_FIELDS + ["validation_status"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 1}),
            "hint": forms.Textarea(attrs={"rows": 1}),
            "answer_explanation": forms.Textarea(attrs={"rows": 3}),
            "answer_book_recommendation": forms.Textarea(attrs={"rows": 1}),
            "answer_image_url_text": forms.Textarea(attrs={"rows": 1}),
            "answer_extra_info": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].queryset = Tag.objects.all().order_by("name")
        self.fields["answer_image_url"].label = _("Answer image")
        # disable some fields
        for field_name in QUESTION_READONLY_FORM_FIELDS:
            self.fields[field_name].disabled = True
        # hide some fields (defaults)
        for field_name in QUESTION_HIDDEN_FORM_FIELDS:
            self.fields[field_name].widget = forms.HiddenInput()
        # required fields
        for field_name in QUESTION_REQUIRED_FORM_FIELDS:
            self.fields[field_name].required = True


class QuestionEditForm(QuestionCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
