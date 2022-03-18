from django.urls import path
from api.views import (
    IndexView, UsersList, UserDetails, AuthUsersList,
    AuthUserDetails, StringsList, StringDetails,
)


app_name = "api"
urlpatterns = [
    path(route="", view=IndexView.as_view(), name="index"),
    path(route="users/", view=UsersList.as_view(), name="users"),
    path(route="users/<str:username>/", view=UserDetails.as_view(), name="user"),
    path(route="auth_users/", view=AuthUsersList.as_view(), name="auth_users"),
    path(route="auth_users/<int:pk>/", view=AuthUserDetails.as_view(), name="auth_user"),
    path(route="strings/", view=StringsList.as_view(), name="strings"),
    path(route="strings/<int:pk>/", view=StringDetails.as_view(), name="string"),
]