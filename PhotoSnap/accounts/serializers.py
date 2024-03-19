from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import RegisterUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate_email(self, value):
        if RegisterUser.objects.filter(email=value).exists():
            raise ValidationError(_("This email address is already in use."))
        return value
    
    def validate_username(self, value):
        if RegisterUser.objects.filter(username=value).exists():
            raise ValidationError(_("This username is already in use."))
        return value
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(_({"password": "Password fields didn't match."}))
        return attrs
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)