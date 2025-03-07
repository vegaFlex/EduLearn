from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = UserProfile
        fields = ["email", "password1", "password2", "role"]

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
