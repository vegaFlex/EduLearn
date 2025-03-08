from django.contrib import admin
from .models import UserProfile, Course, Lesson, Quiz, Question, Review, Order, QuizResult, CompletedLesson


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

# -------------------------------------------------
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "created_at")
    search_fields = ("title", "course__title")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "quiz")
    search_fields = ("question_text", "quiz__title")

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "score", "completed_at")
    search_fields = ("user__email", "quiz__title")
    list_filter = ("score", "completed_at")

@admin.register(CompletedLesson)
class CompletedLessonAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "completed_at")
    search_fields = ("user__email", "lesson__title")
    list_filter = ("completed_at",)

# ------------------------------

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "rating", "created_at", "is_approved")
    search_fields = ("user__username", "course__title")
    list_filter = ("is_approved", "rating", "created_at", "comment")
    actions = ["approve_reviews"]

    @admin.action(description="Одобри избраните ревюта")
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'amount', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('user__email', 'course__title', 'stripe_payment_id')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
