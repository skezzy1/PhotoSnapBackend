from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, confirm_password=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          confirm_password=confirm_password,
          password=password,
          username=username,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user
    
    def create_superuser(self, email, username, password=None, confirm_password=None):
      """
      Creates and saves a superuser with the given email, name, and password.
      """
      user = self.create_user(
          email=email,
          username=username,
          password=password,
          confirm_password=confirm_password,
      )
      user.is_staff = True
      user.is_superuser = True
      user.save(using=self._db)
      return user

class BaseUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name=_("Email address"), max_length=150, unique=True, blank=False)
    username = models.CharField(verbose_name=_('Username'), max_length=150, unique=True, blank=False)
    password = models.CharField(verbose_name=_('Password'), max_length=128, blank=False)
    confirm_password = models.CharField(verbose_name=_('Confirm Password'), max_length=128, blank=False)
    date_joined = models.DateTimeField(verbose_name='Date joined', default=timezone.now)
    last_login = models.DateTimeField(verbose_name='Last login', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_premium = models.BooleanField(default=False, help_text=_('Designates whether the user is a premium user.'))
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'confirm_password']
    def __str__(self): 
         return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_staff

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_admin(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_staff