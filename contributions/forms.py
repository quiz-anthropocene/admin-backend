from django import forms
from django.utils.translation import gettext_lazy as _

from contributions.models import Comment
from core import constants


CONTRIBUTION_STATUS_EDIT_FORM_FIELDS = [
    field.name for field in Comment._meta.fields if field.name not in Comment.CONTRIBUTION_READONLY_FIELDS
]
CONTRIBUTION_REPLY_CREATE_FORM_FIELDS = ["type", "text", "author", "parent", "status"]
CONTRIBUTION_REPLY_HIDDEN_FORM_FIELDS = ["parent", "status"]


class CommentStatusEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = CONTRIBUTION_STATUS_EDIT_FORM_FIELDS
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name not in ["status"]:
                self.fields[field_name].disabled = True


class CommentReplyCreateForm(forms.ModelForm):
    type = forms.ChoiceField(choices=constants.CONTRIBUTION_TYPE_REPLY_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Comment
        fields = CONTRIBUTION_REPLY_CREATE_FORM_FIELDS
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
        for field_name in CONTRIBUTION_REPLY_HIDDEN_FORM_FIELDS:
            self.fields[field_name].widget = forms.HiddenInput()
        # initial values
        self.fields["type"].initial = constants.CONTRIBUTION_TYPE_COMMENT_CONTRIBUTOR
        self.fields["status"].initial = constants.CONTRIBUTION_STATUS_PROCESSED  # ?
        self.fields["text"].label = _("Message")
        self.fields["text"].help_text = None
