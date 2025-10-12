from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Account
from django.core.exceptions import ValidationError

Account = get_user_model()


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = Account
        fields = ['email', 'password', 'confirm_password', 'first_name', 'last_name', 'date_of_birth', 'gender']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")

        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email') 

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and not Account.objects.filter(email=email).exists():
            raise forms.ValidationError("No account found with this email. Please sign up first.")

        return super().clean()
