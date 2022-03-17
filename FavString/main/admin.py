from django.contrib import admin
from main.models import User, AuthUser, String


admin.site.register(User)
admin.site.register(AuthUser)
admin.site.register(String)