from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import BaseUser
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
from django.utils.translation import gettext_lazy as _

class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = BaseUser
        fields=['email', 'username', 'password', 'confirm_password',]
        extra_kwargs={
        'password':{'write_only':True}
         }

  # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        else:
            if len(password) < 8 or len(confirm_password) < 8:
                raise serializers.ValidationError("Too short password")
        return attrs

    def create(self, validate_data):
        return BaseUser.objects.create_user(**validate_data)
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = BaseUser
        fields = ['email', 'password']
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['user_id', 'email', 'username']
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    confirm_password = serializers.CharField(max_length=255, style={'input_type':'confirm_password'}, write_only=True)
    class Meta:
        fields = ['password', 'confirm_password']
        def validate(self, attrs):
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            user = self.context.get('user')
            if password != confirm_password:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            else:
                if len(password) or len(confirm_password) < 8:
                    raise serializers.ValidationError("Too short password")
            user.set_password(password)
            user.make_password(password)
            user.make_password(confirm_password)
            user.save()
            return attrs
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if BaseUser.objects.filter(email=email).exists():
            user = BaseUser.objects.get(email = email)
            user_id = urlsafe_base64_encode(force_bytes(user.user_id))
            print('Encoded UID', user_id)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://0.0.0.0:8000/api/user/send-reset-password-email/'+user_id+'/'+token
            print('Password Reset Link', link)
            # Send EMail
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject':'Reset Your Password',
                'body':body,
                 'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    confirm_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'confirm_password']

def validate(self, attrs):
    try:
      password = attrs.get('password')
      confirm_password = attrs.get('confirm_password')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != confirm_password:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      user_id = smart_str(urlsafe_base64_decode(uid))
      user = BaseUser.objects.get(id=user_id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.make_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')