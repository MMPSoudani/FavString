from main.models import User, AuthUser, String
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = "__all__"

class StringSerializer(serializers.ModelSerializer):
    class Meta:
        model = String
        fields = "__all__"