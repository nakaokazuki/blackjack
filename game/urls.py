from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.top, name="top"),
    path("user/", views.user_page, name="user"),
    path("user/register/", views.SignUpView.as_view(), name="register"),
    path(
        "user/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "user/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path("game/", views.game, name="game"),
]
