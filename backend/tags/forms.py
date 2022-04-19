from ckeditor.widgets import CKEditorWidget
from django import forms

from tags.models import Tag


class TagEditForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Tag
        fields = ["name", "description"]
