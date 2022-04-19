from ckeditor.widgets import CKEditorWidget
from django import forms

from categories.models import Category


class CategoryEditForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Category
        fields = ["name", "name_long", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].disabled = True
