# from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import UserProfile
#
#
# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True, label="Email")
#
#     class Meta:
#         model = UserProfile
#         fields = ["email", "password1", "password2", "role"]
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.username = user.email  # Автоматично попълвам username с email
#         if commit:
#             user.save()
#         return user
#
#
# # class UserLoginForm(AuthenticationForm):
# #     username = forms.EmailField(label="Email")
#
# class UserLoginForm(AuthenticationForm):
#     username = forms.EmailField(widget=forms.EmailInput(attrs={
#         'class': 'w-full px-4 py-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500',
#         'placeholder': 'Email'
#     }))

# from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import UserProfile
#
# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField(
#         required=True,
#         label="Имейл",
#         widget=forms.EmailInput(attrs={
#             'class': 'w-full px-4 py-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500',
#             'placeholder': 'Въведете вашия имейл'
#         })
#     )
#
#     password1 = forms.CharField(
#         label="Парола",
#         widget=forms.PasswordInput(attrs={
#             'class': 'w-full px-4 py-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500',
#             'placeholder': 'Въведете парола'
#         })
#     )
#
#     password2 = forms.CharField(
#         label="Повторете паролата",
#         widget=forms.PasswordInput(attrs={
#             'class': 'w-full px-4 py-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500',
#             'placeholder': 'Повторете паролата'
#         })
#     )
#
#     role = forms.ChoiceField(
#         choices=UserProfile.ROLE_CHOICES,
#         label="Роля",
#         widget=forms.Select(attrs={
#             'class': 'w-full px-4 py-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500'
#         })
#     )
#
#     class Meta:
#         model = UserProfile
#         fields = ["email", "password1", "password2", "role"]
#
#     error_messages = {
#         'password_mismatch': "Паролите не съвпадат! ❌",
#     }
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.username = user.email  # Автоматично попълвам username с email
#         if commit:
#             user.save()
#         return user


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Имейл",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Въведете вашия имейл'
        })
    )

    password1 = forms.CharField(
        label="Парола",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Въведете парола'
        }),
        error_messages={
            "required": "Полето за парола е задължително!",
            "min_length": "Паролата трябва да бъде поне 8 символа!",
            "invalid": "Паролата съдържа неразрешени символи!"
        }
    )

    password2 = forms.CharField(
        label="Повторете паролата",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Повторете паролата'
        }),
        error_messages={
            "required": "Полето за потвърждение на парола е задължително!",
            "min_length": "Паролата трябва да бъде поне 8 символа!",
            "invalid": "Паролата съдържа неразрешени символи!"
        }
    )

    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        label="Роля",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500'
        })
    )

    class Meta:
        model = UserProfile
        fields = ["email", "password1", "password2", "role"]

    error_messages = {
        'password_mismatch': "Паролите не съвпадат! ❌",
    }

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(_("Паролата не отговаря на изискванията: ") + " ".join(e.messages))
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Автоматично попълвам username с email
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Имейл",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Въведете вашия имейл'
        })
    )

    password = forms.CharField(
        label="Парола",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Въведете вашата парола'
        })
    )

    error_messages = {
        "invalid_login": "Грешен имейл или парола. ❌",
        "inactive": "Този акаунт е деактивиран! 🚫",
    }
