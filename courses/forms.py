from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django import forms
from .models import Course

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


# class CourseForm(forms.ModelForm):
#     video_url = forms.URLField(required=False, label="Видео линк", widget=forms.URLInput(attrs={
#         'class': 'w-full px-4 py-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500',
#         'placeholder': 'Въведете URL към видео (YouTube, Vimeo)'
#     }))
#
#     document = forms.FileField(required=False, label="Документ (PDF)", widget=forms.ClearableFileInput(attrs={
#         'class': 'w-full px-4 py-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500'
#     }))
#
#     class Meta:
#         model = Course
#         fields = ["title", "description", "category", "price", "video_url", "document"]
#         labels = {
#             'title': 'Заглавие на курса',
#             'description': 'Описание',
#             'price': 'Цена (лв.)',
#         }
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
#             'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 4}),
#             'price': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
#         }



class CourseForm(forms.ModelForm):
    title = forms.CharField(
        label="Заглавие на курса",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Въведете заглавие'
        })
    )

    description = forms.CharField(
        label="Описание",
        widget=forms.Textarea(attrs={
            'class': 'w-full p-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500',
            'rows': 4,
            'placeholder': 'Опишете курса'
        })
    )

    category = forms.ChoiceField(
        choices=Course.CATEGORY_CHOICES,
        label="Категория",
        widget=forms.Select(attrs={
            'class': 'w-full p-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500'
        })
    )

    price = forms.DecimalField(
        label="Цена (лв.)",
        max_digits=6,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Въведете цена (пример: 49.99)'
        })
    )

    video_url = forms.URLField(
        required=False,
        label="Видео линк",
        widget=forms.URLInput(attrs={
            'class': 'w-full p-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Въведете YouTube/Vimeo линк'
        })
    )

    document = forms.FileField(
        required=False,
        label="Документ (PDF)",
        widget=forms.ClearableFileInput(attrs={
            'class': 'w-full p-3 border border-gray-400 bg-gray-100 text-gray-900 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 file:bg-blue-500 file:text-white file:px-4 file:py-2 file:rounded file:border-none file:cursor-pointer hover:file:bg-blue-700',
        })
    )

    class Meta:
        model = Course
        fields = ["title", "description", "category", "price", "video_url", "document"]
