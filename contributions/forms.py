from django import forms
from django.utils.translation import gettext_lazy as _

from contributions.models import Comment
from core import constants


COMMENT_CREATE_FORM_FIELDS = [
    field.name for field in Comment._meta.fields if field.name not in Comment.COMMENT_READONLY_FIELDS
]
COMMENT_REPLY_CREATE_FORM_FIELDS = ["type", "text", "author", "parent", "status"]
COMMENT_REPLY_HIDDEN_FORM_FIELDS = ["parent", "status"]


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = COMMENT_CREATE_FORM_FIELDS
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ["type", "question", "quiz", "author", "publish"]:
            self.fields[field_name].disabled = True
            # see views.py for exceptions


class CommentEditForm(forms.ModelForm):
    # publish = forms.BooleanField(required=False)

    class Meta:
        model = Comment
        fields = COMMENT_CREATE_FORM_FIELDS
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].disabled = True
            # see views.py for exceptions


class CommentReplyCreateForm(forms.ModelForm):
    type = forms.ChoiceField(choices=constants.COMMENT_TYPE_REPLY_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Comment
        fields = COMMENT_REPLY_CREATE_FORM_FIELDS
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # disable all fields except "text"
        for field_name in self.fields:
            if field_name not in ["text", "type"]:
                self.fields[field_name].disabled = True
        # hide some fields (defaults)
        for field_name in COMMENT_REPLY_HIDDEN_FORM_FIELDS:
            self.fields[field_name].widget = forms.HiddenInput()
        # initial values
        self.fields["type"].initial = constants.COMMENT_TYPE_COMMENT_CONTRIBUTOR
        self.fields["status"].initial = constants.COMMENT_STATUS_PROCESSED
        self.fields["text"].label = _("Message")
        self.fields["text"].help_text = None
