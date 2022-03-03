from django.urls import path
from .views import (
    HomeView, LoginView, RegisterView,
    LogoutView, ProfileOverView, ProfilUpdateView,
    CreateRoomView, RoomView, UpdateRoomView,
    DeleteRoomView, EditMessageView, DeleteMessageView,
)

app_name = "main"
urlpatterns = [
    path(route="", view=HomeView.as_view(), name="home"),
    path(route="login/", view=LoginView.as_view(), name="login"),
    path(route="register/", view=RegisterView.as_view(), name="register"),
    path(route="logout/", view=LogoutView.as_view(), name="logout"),
    path(route="profile/<str:username>/overview/", view=ProfileOverView.as_view(), name="profile_overview"),
    path(route="profile/<str:username>/update/", view=ProfilUpdateView.as_view(), name="profile_update"),
    path(route="ceate_room/", view=CreateRoomView.as_view(), name="create_room"),
    path(route="room/<str:title>/", view=RoomView.as_view(), name="room"),
    path(route="room/<str:title>/update_room/", view=UpdateRoomView.as_view(), name="update_room"),
    path(route="room/<str:title>/delete_room/", view=DeleteRoomView.as_view(), name="del_room"),
    path(route="room/<str:title>/msg/<str:pk>/edit_msg/", view=EditMessageView.as_view(), name="edit_msg"),
    path(route="room/<str:title>/msg/<str:pk>/delete_msg/", view=DeleteMessageView.as_view(), name="del_msg"),
]