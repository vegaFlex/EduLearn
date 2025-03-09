from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CourseForm
from django.db.models import  Avg, Q  # Импортирам за търсене с OR
from django.http import JsonResponse
import stripe
from django.urls import reverse
from django.conf import settings
from .models import Quiz, Question, QuizResult, CompletedLesson, Lesson, Course, Order, Review
from .forms import ReviewForm

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    return render(request, "index.html")  # ще използва index.html за начална страница


# def courses_list(request):
#     courses = Course.objects.all()
#     return render(request, "courses.html", {"courses": courses})

def courses_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    min_rating = request.GET.get('rating')  # Взимам стойността на рейтинга от заявката

    # courses = Course.objects.all()
    courses = Course.objects.annotate(average_rating=Avg("reviews__rating"))  # Анотация за среден рейтинг

    if query:
        courses = courses.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if category:
        courses = courses.filter(category=category)

    if min_price:
        courses = courses.filter(price__gte=min_price)

    if max_price:
        courses = courses.filter(price__lte=max_price)

    if min_rating:  # Филтър по рейтинг
        courses = courses.filter(rating__gte=min_rating)

    return render(request, "courses.html", {
        "courses": courses,
        "query": query,
        "category": category,
        "min_price": min_price,
        "max_price": max_price,
        "min_rating": min_rating,
    })


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
    # Само преподавателите могат да създават курсове
    if request.user.role != 'teacher':
        messages.error(request, "Само преподаватели могат да създават курсове! ❌")
        return redirect("courses")

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)  # Добавено request.FILES за качване на файлове
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


# def course_detail(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     return render(request, "course_detail.html", {"course": course})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()  # Взимаме всички уроци за този курс

    return render(request, "course_detail.html", {
        "course": course,
        "lessons": lessons,
        "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY
    })


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


@login_required
def create_checkout_session(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Създавам Stripe Checkout сесия
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "bgn",
                    "product_data": {
                        "name": course.title,
                    },
                    "unit_amount": int(course.price * 100),  # Цената в стотинки
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(reverse("payment_success")) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("payment_cancel")),
    )

    # създавам поръчка в базата данни
    order = Order.objects.create(
        user=request.user,
        course=course,
        amount=course.price,
        stripe_payment_id=session.id,
        is_paid=False,
    )

    return JsonResponse({"sessionId": session.id})


def payment_success(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return redirect("courses")

    # проверка дали поръчката съществува
    order = get_object_or_404(Order, stripe_payment_id=session_id)
    order.is_paid = True
    order.save()

    # записвам потребителя в курса
    order.course.students.add(order.user)

    messages.success(request, "Успешно платихте курса!")
    # return redirect("profile")
    return render(request, "payment_success.html", {
        "order": order
    })


def payment_cancel(request):
    messages.error(request, "Плащането беше отменено.")
    return redirect("courses")


@login_required
def my_courses(request):
    courses = request.user.enrolled_courses.all()  # всички курсове, в които е записан потребителят
    return render(request, "my_courses.html", {"courses": courses})



@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == "POST":
        score = 0
        total_questions = questions.count()

        for question in questions:
            selected_answer = request.POST.get(f"question_{question.id}")
            if selected_answer and selected_answer == question.correct_answer:
                score += 1

        final_score = int((score / total_questions) * 100)
        QuizResult.objects.create(user=request.user, quiz=quiz, score=final_score)

        messages.success(request, f"Тестът е завършен! Вашият резултат: {final_score}%")
        return redirect("my_courses")

    return render(request, "quiz_detail.html", {"quiz": quiz, "questions": questions})

@login_required
def mark_lesson_completed(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    CompletedLesson.objects.get_or_create(user=request.user, lesson=lesson)
    messages.success(request, "Урокът е маркиран като завършен! ✅")
    return redirect("my_courses")


@login_required
def add_review(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.course = course
            review.is_approved = False  # всички ревюта трябва да бъдат одобрени от админ
            review.save()
            messages.info(request, "Вашето ревю беше изпратено за одобрение! ✅")
            # messages.success(request, "Вашето ревю беше добавено успешно!")
            return redirect('course_detail', course_id=course.id)
    else:
        form = ReviewForm()

    return render(request, "add_review.html", {"form": form, "course": course})
