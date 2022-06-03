from django import forms

from questions.models import Question
from questions.tables import QUESTION_FIELD_SEQUENCE
from tags.models import Tag


QUESTION_READONLY_FORM_FIELDS = ["author", "validation_status"]
QUESTION_REQUIRED_FORM_FIELDS = ["answer_option_a", "answer_option_b", "answer_correct"]
QUESTION_FORM_FIELDS = [
    field_name for field_name in QUESTION_FIELD_SEQUENCE if field_name not in Question.QUESTION_READONLY_FIELDS
]


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = QUESTION_FORM_FIELDS + QUESTION_READONLY_FORM_FIELDS
        widgets = {
            "text": forms.Textarea(attrs={"rows": 1}),
            "hint": forms.Textarea(attrs={"rows": 1}),
            "answer_explanation": forms.Textarea(attrs={"rows": 3}),
            "answer_reading_recommendation": forms.Textarea(attrs={"rows": 1}),
            "answer_image_url": forms.HiddenInput(),
            "answer_image_explanation": forms.Textarea(attrs={"rows": 1}),
            "answer_extra_info": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].queryset = Tag.objects.all().order_by("name")
        for field_name in QUESTION_READONLY_FORM_FIELDS:
            self.fields[field_name].disabled = True
        for field_name in QUESTION_REQUIRED_FORM_FIELDS:
            self.fields[field_name].required = True


class QuestionEditForm(QuestionCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["validation_status"].disabled = False
