from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = UserProfile
        fields = ["email", "password1", "password2", "role"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Автоматично попълвам username с email
        if commit:
            user.save()
        return user


# class UserLoginForm(AuthenticationForm):
#     username = forms.EmailField(label="Email")

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500',
        'placeholder': 'Email'
    }))
