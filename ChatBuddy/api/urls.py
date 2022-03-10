from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import (
    UsersList, UserDetails, ProfilesList, ProfileDetails,
    TopicsList, TopicDetails, RoomsList, RoomDetails,
    MessagesList, MessageDetails, IndexView,
)


app_name = "api"
urlpatterns = [
    path(route="", view=IndexView.as_view(), name="index"),
    path(route="users/", view=UsersList.as_view(), name="users"),
    path(route="users/<str:pk>/", view=UserDetails.as_view(), name="user"),
    path(route="profiles/", view=ProfilesList.as_view(), name="profiles"),
    path(route="profiles/<str:pk>/", view=ProfileDetails.as_view(), name="profile"),
    path(route="topics/", view=TopicsList.as_view(), name="topics"),
    path(route="topics/<str:pk>/", view=TopicDetails.as_view(), name="topic"),
    path(route="rooms/", view=RoomsList.as_view(), name="rooms"),
    path(route="rooms/<str:pk>/", view=RoomDetails.as_view(), name="room"),
    path(route="messages/", view=MessagesList.as_view(), name="messages"),
    path(route="messages/<str:pk>/", view=MessageDetails.as_view(), name="message"),
]

urlpatterns = format_suffix_patterns(urlpatterns)