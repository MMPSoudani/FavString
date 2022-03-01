from django.contrib import admin
from .models import User, Profile, Topic, Room, Message


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Message)