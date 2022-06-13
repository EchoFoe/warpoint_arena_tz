from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from authentication.models import User


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
JWT_AUTH_HEADER_PREFIX = api_settings.JWT_AUTH_HEADER_PREFIX


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                '! - Пользователь с данной электронной почтой и паролем не найден'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            jwt_prefix = JWT_AUTH_HEADER_PREFIX
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                '! - Пользователь с данной электронной почтой и паролем не существует'
            )
        return {
            'email': user.email,
            'prefix': jwt_prefix,
            'token': jwt_token
        }
