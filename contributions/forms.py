from django import forms

from contributions.models import Contribution


CONTRIBUTION_STATUS_EDIT_FORM_FIELDS = [
    field.name for field in Contribution._meta.fields if field.name not in Contribution.CONTRIBUTION_READONLY_FIELDS
]


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
