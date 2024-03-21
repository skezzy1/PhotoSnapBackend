from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager

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

class BaseUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name=_("Email address"), max_length=150, unique=True, blank=False)
    username = models.SlugField(verbose_name=_('Username'), max_length=150, unique=True, blank=False)
    password = models.CharField(verbose_name=_('Password'), max_length=128, blank=False)
    confirm_password = models.CharField(verbose_name=_('Confirm Password'), max_length=128, blank=False)
    date_joined = models.DateTimeField(verbose_name='Date joined', default=timezone.now)
    last_login = models.DateTimeField(verbose_name='Last login', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_premium = models.BooleanField(default=False, help_text=_('Designates whether the user is a premium user.'))
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
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def clean(self):
        if BaseUser.objects.filter(email=self.email).exists():
            raise ValidationError({'email': _('This email address is already in use.')})
        if BaseUser.objects.filter(username=self.username).exists():
            raise ValidationError({'username':_('This username is already in use.')})
        super().clean()
