from django.urls import path
from .views import courses_list

urlpatterns = [
    path("courses/", courses_list, name="courses"),
]
