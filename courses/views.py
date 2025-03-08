from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Course
from .forms import CourseForm


def index(request):
    return render(request, "index.html")  # ще използва index.html за начална страница

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


@login_required
def create_course(request):
    #Само преподавателите могат да създават курсове
    if request.user.role != 'teacher':
        messages.error(request, "Само преподаватели могат да създават курсове! ❌")
        return redirect("courses")

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)  #Добавено request.FILES за качване на файлове
        if form.is_valid():
            course = form.save(commit=False)
            course.creator = request.user  # Задавам текущия потребител като създател
            course.save()
            messages.success(request, "Курсът беше създаден успешно! ✅")
            return redirect("courses")
        else:
            messages.error(request, "Моля, поправете грешките във формата. ❌")
    else:
        form = CourseForm()

    return render(request, "create_course.html", {"form": form})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, "course_detail.html", {"course": course})


@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user != course.creator:
        messages.error(request, "Нямате право да редактирате този курс! ❌")
        return redirect("courses")

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Курсът беше успешно редактиран! ✅")
            return redirect("courses")
    else:
        form = CourseForm(instance=course)

    return render(request, "edit_course.html", {"form": form, "course": course})


@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Проверявам дали текущият потребител е създателят на курса
    if request.user != course.creator:
        messages.error(request, "Нямате право да изтривате този курс! ❌")
        return redirect("courses")

    if request.method == "POST":
        course.delete()
        messages.success(request, "Курсът беше успешно изтрит! 🗑")
        return redirect("courses")

    return render(request, "delete_course.html", {"course": course})
