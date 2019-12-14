from django.contrib import admin
from django.urls import path, include
from api import urls

urlpatterns = [
    path("admin/", admin.site.urls), 
    path("api/v1/", include(urls)),
    path("api/v1/auth", include("knox.urls"))
]