from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import BaseUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
class UserModelAdmin(BaseUserAdmin):
    list_display = ('user_id', 'email', 'username', 'password','last_login','date_joined', 'is_premium', 'is_staff', 'last_login')
    list_filter = ('is_staff',) 
    fieldsets = (
        ('User Credentials', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'last_login')}),
        ('Permissions', {'fields': ('is_staff', 'is_premium')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()
    def __str__(self):
        return self.email
admin.site.register(BaseUser, UserModelAdmin)
