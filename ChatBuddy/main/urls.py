from django.urls import path
from .views import (
    HomeView,
)

app_name = "main"
urlpatterns = [
    path(route="", view=HomeView.as_view(), name="home"),
]