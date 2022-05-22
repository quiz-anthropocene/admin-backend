from django import forms

from contributions.models import Contribution
from core import constants


CONTRIBUTION_STATUS_EDIT_FORM_FIELDS = [
    field.name for field in Contribution._meta.fields if field.name not in Contribution.CONTRIBUTION_READONLY_FIELDS
]
CONTRIBUTION_REPLY_CREATE_FORM_FIELDS = ["parent", "text", "type", "author", "status"]


class ContributionStatusEditForm(forms.ModelForm):
    class Meta:
        model = Contribution
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


class ContributionReplyCreateForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = CONTRIBUTION_REPLY_CREATE_FORM_FIELDS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # disable all fields except "text"
        for field_name in self.fields:
            if field_name not in ["text"]:
                self.fields[field_name].disabled = True
        # hide some fields (defaults)
        for field_name in ["parent", "type", "status"]:
            self.fields[field_name].widget = forms.HiddenInput()
        # initial values
        self.fields["type"].initial = constants.CONTRIBUTION_TYPE_REPLY
        self.fields["status"].initial = constants.CONTRIBUTION_STATUS_PROCESSED  # ?
        self.fields["text"].label = "Réponse"
        self.fields["text"].help_text = None
