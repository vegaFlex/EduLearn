from django.urls import path
from .views import courses_list, register, login_view, logout_view, profile, payment_success, payment_cancel
from .views import create_checkout_session, create_course, course_detail, edit_course, delete_course, my_courses

urlpatterns = [
    path("courses/", courses_list, name="courses"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile, name="profile"),
    path("create/", create_course, name="create_course"),
    path("courses/<int:course_id>/", course_detail, name="course_detail"),
    path("edit/<int:course_id>/", edit_course, name="edit_course"),
    path("delete/<int:course_id>/", delete_course, name="delete_course"),
    path("checkout/<int:course_id>/", create_checkout_session, name="create_checkout_session"),
    path("payment-success/", payment_success, name="payment_success"),
    path("payment-cancel/", payment_cancel, name="payment_cancel"),
    path("my-courses/", my_courses, name="my_courses"),

]
