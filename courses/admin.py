from django.contrib import admin
from .models import UserProfile, Course, Lesson, Quiz, Question, Review, Order


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "creator", "created_at")
    list_filter = ("category", "price")
    search_fields = ("title", "creator__username")
    ordering = ('-created_at',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "created_at")
    search_fields = ("title", "course__title")


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "created_at")
    search_fields = ("title", "course__title")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "quiz")
    search_fields = ("question_text", "quiz__title")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "rating", "created_at")
    search_fields = ("user__username", "course__title")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'amount', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('user__email', 'course__title', 'stripe_payment_id')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
