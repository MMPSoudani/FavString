from django .urls import path
from main.views import (
    HomeView, LoginView, RegisterView, LogoutView, AddStringView,
    StringOverView,
)


app_name = "main"
urlpatterns = [
    path(route="", view=HomeView.as_view(), name="home"),
    path(route="login/", view=LoginView.as_view(), name="login"),
    path(route="register/", view=RegisterView.as_view(), name="register"),
    path(route="logout/", view=LogoutView.as_view(), name="logout"),
    path(route="add_string/", view=AddStringView.as_view(), name="add_string"),
    path(route="string/<str:id>/overview/", view=StringOverView.as_view(), name="string_overview"),
]