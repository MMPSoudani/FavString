from django.urls import path
from .views import (
    HomeView, LoginView, RegisterView,
    LogoutView,
)

app_name = "main"
urlpatterns = [
    path(route="", view=HomeView.as_view(), name="home"),
    path(route="login/", view=LoginView.as_view(), name="login"),
    path(route="register/", view=RegisterView.as_view(), name="register"),
    path(route="logout/", view=LogoutView.as_view(), name="logout"),
]