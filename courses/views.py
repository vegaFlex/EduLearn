from .models import Course
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model


def courses_list(request):
    courses = Course.objects.all()
    return render(request, "courses.html", {"courses": courses})


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Успешно се регистрирахте! 🎉")
            return redirect("courses")
        else:
            # messages.error(request, "Моля, поправете грешките във формата. ❌")
            # Добавям грешките на формата като съобщения
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserRegistrationForm()
    return render(request, "register.html", {"form": form})


# def login_view(request):
#     if request.method == "POST":
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             messages.success(request, f"Добре дошъл, {user.email}! 😊")
#             return redirect("courses")
#         else:
#             messages.error(request, "Грешен email или парола. ❌")
#     else:
#         form = UserLoginForm()
#     return render(request, "login.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        email = request.POST.get("username")  # Django все още очаква "username", но използвам email
        password = request.POST.get("password")

        # Трябва да вземем потребителя по email, защото authenticate() очаква username
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):
            login(request, user)
            messages.success(request, f"Добре дошъл, {user.email}! 😊")
            return redirect("courses")
        else:
            messages.error(request, "Грешен email или парола. ❌")

    else:
        form = UserLoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Успешно излязохте от профила си.")
    return redirect("login")


@login_required
def profile(request):
    return render(request, "profile.html", {"user": request.user})
