from django import forms

from glossary.models import GlossaryItem


GLOSSARY_ITEM_FORM_FIELDS = [
    field.name for field in GlossaryItem._meta.fields if field.name not in GlossaryItem.GLOSSARY_ITEM_READONLY_FIELDS
]


class GlossaryItemCreateForm(forms.ModelForm):
    class Meta:
        model = GlossaryItem
        fields = GLOSSARY_ITEM_FORM_FIELDS
        widgets = {
            "name_alternatives": forms.Textarea(attrs={"rows": 1}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class GlossaryItemEditForm(GlossaryItemCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].disabled = True
