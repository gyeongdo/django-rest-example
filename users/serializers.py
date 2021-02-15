from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *

# 접속 유지중인지 확인할 시리얼라이저


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name")


class CreateUserSerializer(serializers.ModelSerializer):
    # profile = AddProfileSerializer()
    class Meta:
        model = User
        fields = ("id", "username", "password", "email")
        extra_kwargs = {"password": {"write_only": True}}

    # def create(self, validated_data):
    #     user = User.objects.create_user(
    #           validated_data["username"]
    #         , validated_data["email"]
    #         , validated_data["password"]
    #     )
    #     return user

# 로그인 시리얼라이저

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        print("data : ", data)
        user = authenticate(**data)
        print('user : ', user.is_active)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("user_pk", "nickname", "phone", "email")