from django.contrib import admin
from .models import Section, Shift, Schedule, DirectManager, Status, Role, Employee
from django.contrib.auth.models import Permission


admin.site.register(Permission)

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
    list_display = ('hr_name','role', 'is_active')
    list_filter = ['is_active', 'role','direct_manager','section' ]
    search_fields = ['hr_name',]
    ordering = ('created_at',)
