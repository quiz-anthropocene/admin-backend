from django import forms

from glossary.models import GlossaryItem


class GlossaryItemCreateForm(forms.ModelForm):
    class Meta:
        model = GlossaryItem
        fields = "__all__"
        widgets = {
            "name_alternatives": forms.Textarea(attrs={"rows": 1}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }
