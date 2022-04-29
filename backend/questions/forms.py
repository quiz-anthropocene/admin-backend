from django import forms

from questions.models import Question
from questions.tables import QUESTION_FIELD_SEQUENCE
from tags.models import Tag


QUESTION_FORM_FIELDS = [
    field_name for field_name in QUESTION_FIELD_SEQUENCE if field_name not in Question.QUESTION_READONLY_FIELDS
]


class QuestionEditForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = QUESTION_FORM_FIELDS
        widgets = {
            "text": forms.Textarea(attrs={"rows": 2}),
            "hint": forms.Textarea(attrs={"rows": 2}),
            "answer_explanation": forms.Textarea(attrs={"rows": 4}),
            "answer_reading_recommendation": forms.Textarea(attrs={"rows": 2}),
            "answer_image_explanation": forms.Textarea(attrs={"rows": 2}),
            "answer_extra_info": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].queryset = Tag.objects.all().order_by("name")
