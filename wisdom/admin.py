# wisdom/admin.py
from django.contrib import admin
from .models import Wisdom

@admin.register(Wisdom)
class WisdomAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_active',)
    list_filter = ['is_active','author',]
    search_fields = ['author',]
    ordering = ('text',)
