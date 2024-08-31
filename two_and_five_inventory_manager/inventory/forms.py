from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    usable_password = None # removes the password authentication display.

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
