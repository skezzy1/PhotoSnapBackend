from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import BaseUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class BaseUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = BaseUser
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        if BaseUser.objects.filter(email=value).exists():
            raise ValidationError(_("This {email} address is already in use."))
        return value
    
    def validate_username(self, value):
        if BaseUser.objects.filter(username=value).exists():
            raise ValidationError(_("This {username} is already in use."))
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if len(attrs['password']) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})
        return attrs

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return BaseUser.objects.create_user(**validated_data)
