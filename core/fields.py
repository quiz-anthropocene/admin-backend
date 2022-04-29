from django import forms
from django.contrib.postgres.fields import ArrayField


# https://stackoverflow.com/a/66059615/4293684
class ChoiceArrayField(ArrayField):
    """
    Custom ArrayField with a ChoiceField as default field.
    The default field is a comma-separated InputText, which is not very useful.
    """

    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.TypedMultipleChoiceField,
            "choices": self.base_field.choices,
            "coerce": self.base_field.to_python,
            "widget": forms.CheckboxSelectMultiple,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)
