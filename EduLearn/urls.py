from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from courses.views import index
from courses.admin import admin_site  # Използвам CustomAdminSite

urlpatterns = [
                  # path("admin/", admin.site.urls),
                  path("admin/", admin_site.urls),  # Използвам admin_site вместо admin.site
                  path("", index, name="home"),  # Това пренасочва към  index.html
                  # path("", courses_list, name="home"),  # Началната страница вече ще показва курсовете
                  path("", include("courses.urls")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
