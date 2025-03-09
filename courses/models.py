from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.contrib.auth import get_user_model

# User = get_user_model()


class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Имейлът е задължителен!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Преподавател'),
        ('student', 'Ученик'),
    )

    email = models.EmailField(unique=True)  # Email ще бъде уникален и ще служи за вход
    username = models.CharField(max_length=150, blank=True, null=True,
                                unique=True)  # username няма да се ползва активно


    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name="user_profiles", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="user_profiles_permissions", blank=True)

    USERNAME_FIELD = "email"  # Влизам с email вместо username
    REQUIRED_FIELDS = []  # Django очаква допълнителни задължителни полета, но ги премахвам

    objects = UserProfileManager()  # Добавям новия мениджър

    # def save(self, *args, **kwargs):
    #     if not self.username:
    #         self.username = self.email  # Ако username е празно, попълвам го с email
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class Course(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Програмиране'),
        ('design', 'Дизайн'),
        ('marketing', 'Маркетинг'),
        ('business', 'Бизнес'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    # creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="enrolled_courses",
                                      blank=True)

    video_url = models.URLField(blank=True, null=True)  # Позволява линкове към YouTube/Vimeo
    document = models.FileField(upload_to="course_documents/", blank=True, null=True)  # Качване на PDF файлове

    created_at = models.DateTimeField(auto_now_add=True)

    # rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], blank=True,
                               null=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=255)
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

class QuizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.quiz.title} ({self.score}%)"

class CompletedLesson(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey("Lesson", on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "lesson")

    def __str__(self):
        return f"{self.user.email} - {self.lesson.title} (Completed)"


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({self.rating})"

class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="orders")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="orders")
    amount = models.DecimalField(max_digits=6, decimal_places=2)  # Цена на курса
    stripe_payment_id = models.CharField(max_length=255, blank=True, null=True)  # ID на Stripe плащането
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Поръчка: {self.user.email} - {self.course.title} - {self.amount} лв."
