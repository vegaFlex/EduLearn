from django.contrib import admin
from .models import UserProfile, Course, Lesson, Quiz, Question, Review, Order, QuizResult, CompletedLesson
from django.urls import path
from django.contrib.admin import AdminSite
from django.shortcuts import render
from django.db.models import Count, Sum
from django.utils.safestring import mark_safe
import json
from .models import SliderImage


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_active", "date_joined")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "creator", "created_at", "total_orders")
    list_filter = ("category", "price")
    search_fields = ("title", "creator__username", "category")
    ordering = ('-created_at',)

    def total_orders(self, obj):
        return obj.orders.count()

    total_orders.short_description = "Брой записани студенти"


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

#
# class CustomAdminSite(AdminSite):
#     site_header = "EduLearn Администрация"
#     site_title = "Админ панел"
#     index_title = "Добре дошли в администрацията"
#
#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path("dashboard/", self.admin_view(self.dashboard), name="dashboard"),
#         ]
#         return custom_urls + urls
#
#     def dashboard(self, request):
#         total_users = UserProfile.objects.count()
#         total_courses = Course.objects.count()
#         total_orders = Order.objects.filter(is_paid=True).count()
#         total_revenue = Order.objects.filter(is_paid=True).aggregate(Sum("amount"))["amount__sum"] or 0
#
#         context = {
#             "total_users": total_users,
#             "total_courses": total_courses,
#             "total_orders": total_orders,
#             "total_revenue": total_revenue,
#         }
#         return render(request, "admin/dashboard.html", context)
#
# admin_site = CustomAdminSite(name="custom_admin")
# admin_site.register(Course, CourseAdmin)
# admin_site.register(Order, OrderAdmin)
# admin_site.register(UserProfile, UserProfileAdmin)
# admin_site.register(CompletedLesson, CompletedLessonAdmin)


#
# class CustomAdminSite(AdminSite):
#     site_header = "EduLearn Администрация"
#     site_title = "Админ панел"
#     index_title = "Добре дошли в администрацията"
#
#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path("dashboard/", self.admin_view(self.dashboard), name="dashboard"),
#         ]
#         return custom_urls + urls
#
#     def dashboard(self, request):
#         total_users = UserProfile.objects.count()
#         total_courses = Course.objects.count()
#         total_orders = Order.objects.filter(is_paid=True).count()
#         total_revenue = Order.objects.filter(is_paid=True).aggregate(Sum("amount"))["amount__sum"] or 0
#
#         # ✅ Данни за приходи по месеци (примерно генерирани)
#         revenue_data = [1200, 1800, 1400, 2000, 1700]  # Примерни приходи за 5 месеца
#         revenue_labels = ["Януари", "Февруари", "Март", "Април", "Май"]
#
#         # ✅ Най-популярни курсове по брой поръчки
#         popular_courses = Course.objects.annotate(num_orders=Count("orders")).order_by("-num_orders")[:5]
#         popular_labels = [course.title for course in popular_courses]
#         popular_data = [course.num_orders for course in popular_courses]
#
#         context = {
#             "total_users": total_users,
#             "total_courses": total_courses,
#             "total_orders": total_orders,
#             "total_revenue": total_revenue,
#             "revenue_labels": mark_safe(json.dumps(revenue_labels)),
#             "revenue_data": mark_safe(json.dumps(revenue_data)),
#             "popular_labels": mark_safe(json.dumps(popular_labels)),
#             "popular_data": mark_safe(json.dumps(popular_data)),
#         }
#         return render(request, "admin/dashboard.html", context)

@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'text', 'course__title')

# ==============================================================

class CustomAdminSite(AdminSite):
    site_header = "EduLearn Администрация"
    site_title = "Админ панел"
    index_title = "Добре дошли в администрацията"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("dashboard/", self.admin_view(self.dashboard), name="dashboard"),
        ]
        return custom_urls + urls

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["dashboard_url"] = "/admin/dashboard/"
        return super().index(request, extra_context)

    def dashboard(self, request):
        total_users = UserProfile.objects.count()
        total_courses = Course.objects.count()
        total_orders = Order.objects.filter(is_paid=True).count()
        total_revenue = Order.objects.filter(is_paid=True).aggregate(Sum("amount"))["amount__sum"] or 0

        # Данни за приходи по месеци (примерно генерирани)
        revenue_data = [1200, 1800, 1400, 2000, 1700]  # Примерни приходи за 5 месеца
        revenue_labels = ["Януари", "Февруари", "Март", "Април", "Май"]

        # Най-популярни курсове по брой поръчки
        popular_courses = Course.objects.annotate(num_orders=Count("orders")).order_by("-num_orders")[:5]
        popular_labels = [course.title for course in popular_courses]
        popular_data = [course.num_orders for course in popular_courses]

        context = {
            "total_users": total_users,
            "total_courses": total_courses,
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "revenue_labels": mark_safe(json.dumps(revenue_labels)),
            "revenue_data": mark_safe(json.dumps(revenue_data)),
            "popular_labels": mark_safe(json.dumps(popular_labels)),
            "popular_data": mark_safe(json.dumps(popular_data)),
        }
        return render(request, "admin/dashboard.html", context)

# импортирам CustomAdminSite и регистрирам моделите
admin_site = CustomAdminSite(name="custom_admin")

# регистрирам ВСИЧКИ модели в CustomAdminSite
admin_site.register(UserProfile, UserProfileAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson, LessonAdmin)
admin_site.register(Quiz, QuizAdmin)
admin_site.register(Question, QuestionAdmin)
admin_site.register(QuizResult, QuizResultAdmin)
admin_site.register(Order, OrderAdmin)
admin_site.register(Review, ReviewAdmin)
admin_site.register(CompletedLesson, CompletedLessonAdmin)
admin_site.register(SliderImage, SliderImageAdmin)


# ========================================================================




