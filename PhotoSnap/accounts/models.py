from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class RegisterUser(AbstractBaseUser):
    USERNAME_FIELD = 'username'
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name=_("Email address"), max_length=150, unique=True, blank=False)
    username = models.SlugField(verbose_name=_('Username'),max_length=150, unique=True, blank=False)
    password = models.CharField(verbose_name=_('Password'), max_length=128, blank=False)
    confirm_password = models.CharField(verbose_name=_('Confirm Password'), max_length=128, blank=False)
    date_joined = models.DateTimeField(verbose_name='Date joined', default=timezone.now)
    last_login = models.DateTimeField(verbose_name='Last login', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, help_text=_('Designates whether the user can log into this admin site.'))
    def save(self, *args, **kwargs):
        if self.password != self.confirm_password:
            raise ValidationError(_("Password and confirm password do not match"))
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
    def clean(self):
        super().clean()
        if RegisterUser.objects.filter(email=self.email).exists():
            raise ValidationError({'email': _('This email address is already in use.')})
        if RegisterUser.objects.filter(username=self.username).exists():
            raise ValidationError({'username':_('This username is already in use.')})
