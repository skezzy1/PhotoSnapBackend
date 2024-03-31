from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import BaseUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
<<<<<<< HEAD

class UserModelAdmin(BaseUserAdmin):
    list_display = ('user_id', 'email', 'username', 'password', 'last_login', 'date_joined', 'is_premium')
=======
class UserModelAdmin(BaseUserAdmin):
    list_display = ('user_id', 'email', 'username', 'password','last_login','date_joined', 'is_premium', 'is_staff', 'last_login')
>>>>>>> origin/bugFix
    list_filter = ('is_staff',) 
    fieldsets = (
        ('User Credentials', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'last_login')}),
        ('Permissions', {'fields': ('is_staff', 'is_premium')}),
    )
    add_fieldsets = (
<<<<<<< HEAD
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password')}
=======
        ('Add User',{
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'confirm_password')}
>>>>>>> origin/bugFix
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()
<<<<<<< HEAD

admin.site.register(BaseUser, UserModelAdmin)
=======
    def __str__(self):
        return self.email
admin.site.register(BaseUser)
>>>>>>> origin/bugFix
