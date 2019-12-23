from django.urls import path, include
from .views import RegistrationAPI, LoginAPI, UserAPI, TodayListAPI, ContactViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register('contact', ContactViewSet)

urlpatterns = [
    path("auth/register/", RegistrationAPI.as_view()),
    path("auth/login/", LoginAPI.as_view()),
    path("user/", UserAPI.as_view()),
    path("", include(router.urls)),
    path("today/", TodayListAPI.as_view(), name= 'posts_filter')
]