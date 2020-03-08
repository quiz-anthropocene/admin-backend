from django.contrib import admin
from django.urls import path, include

from app import views


urlpatterns = [
    path("", views.app_home),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]
