from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager

<<<<<<< HEAD
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
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
          confirm_password=confirm_password,
          username=username,
      )
      user.is_admin = True
      user.save(using=self._db)
      return user
=======
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            username=username,
            password=password,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
    
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)
>>>>>>> origin/bugFix

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
<<<<<<< HEAD
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'confirm_password']
    def __str__(self): 
         return self.email

    def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

    def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

    @property
    def is_admin(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_staff
=======
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'confirm_password']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_superuser

    def has_module_perms(self, admin_site):
        "Does the user have permissions to view the app 'admin'?"
        return True

    @property
    def is_admin(self):
        "Is the user a member of staff?"
        return self.is_staff

    def validation(self, *args, **kwargs):
        if self.password and self.confirm_password != self.password:
            raise ValidationError(_("Password and confirm password do not match"))
        if len(self.password or self.confirm_password) < 8:
            raise ValidationError(_({"password": "Password must be at least 8 characters long."}))
        self.password = make_password(self.password)
        self.confirm_passwordpassword = make_password(self.confirm_password)
        super().save(*args, **kwargs)

    def clean(self):
        if BaseUser.objects.filter(email=self.email).exists():
            raise ValidationError({'email': _('This email address is already in use.')})
        if BaseUser.objects.filter(username=self.username).exists():
            raise ValidationError({'username':_('This username is already in use.')})
        super().clean()
>>>>>>> origin/bugFix
