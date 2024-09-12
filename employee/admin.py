from django.contrib import admin
from .models import Section, Shift, Schedule, DirectManager, Status, Role, Employee


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    ordering = ('name',)


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    ordering = ('name',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'shift')
    ordering = ('name',)


@admin.register(DirectManager)
class DirectManagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    ordering = ('name',)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    ordering = ('name',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    ordering = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_english_name', 'hr_name', 'section', 'shift', 'direct_manager', 'role', 'status')
    ordering = ('created_at',)
