from django.urls import path
from .views import courses_list, register, login_view, logout_view, profile

urlpatterns = [
    path("courses/", courses_list, name="courses"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile, name="profile"),
]
