from ckeditor.widgets import CKEditorWidget
from django import forms

from tags.models import Tag


class TagCreateForm(forms.ModelForm):
    description = forms.CharField(required=False, widget=CKEditorWidget())

    class Meta:
        model = Tag
        fields = ["name", "description"]


class TagEditForm(TagCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].disabled = True
