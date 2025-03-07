from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.urls import include


def index(request):
    return render(request, "index.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="home"),
    path("", include("courses.urls")),
]
