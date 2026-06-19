from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display    = ('email', 'full_name', 'role', 'is_verified', 'is_active')
    list_filter     = ('role', 'is_verified', 'is_active')
    search_fields   = ('email', 'full_name', 'phone')
    ordering        = ('created_at',)
    fieldsets       = (
        (None,           {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone', 'profile_photo')}),
        ('Role & Status', {'fields': ('role', 'is_verified', 'is_active', 'is_staff')}),
        ('Permissions',  {'fields': ('groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone', 'role', 'password1', 'password2'),
        }),
    )