from django import forms

from users.models import User


class ContributorCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "roles"]  # password auto-generated in admin/views.py

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["roles"].required = True
