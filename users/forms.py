from django import forms

from users.models import User, UserCard


class ProfileInfoCardCreateForm(forms.ModelForm):
    class Meta:
        model = UserCard
        fields = ["short_biography", "quiz_relationship", "website_url"]


class ContributorCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "roles"]  # password auto-generated in admin/views.py

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["roles"].required = True
