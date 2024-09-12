from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'is_active', 'is_staff')
    search_fields = ('username',)
    readonly_fields = ('companies', 'role')

admin.site.register(CustomUser, CustomUserAdmin)
