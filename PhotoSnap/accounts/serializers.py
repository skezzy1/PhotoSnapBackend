from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import BaseUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate_email(self, value):
        if BaseUser.objects.filter(email=value).exists():
            raise ValidationError(_("This {email} address is already in use."))
        return value
    
    def validate_username(self, value):
        if BaseUser.objects.filter(username=value).exists():
            raise ValidationError(_("This {username} is already in use."))
        return value
    def validate_password(self, attrs, validated_data):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(_({"password": "Password fields didn't match."}))
        if len(attrs['password']) < 8:
            raise serializers.ValidationError(_({"password": "Password must be at least 8 characters long."}))
        validated_data['password'] = make_password(validated_data['password'])
        return attrs and super().create(validated_data)