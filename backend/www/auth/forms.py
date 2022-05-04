from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm


class LoginForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data["username"]
        return username.lower()


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Votre adresse e-mail", required=True)
