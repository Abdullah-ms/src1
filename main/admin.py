from django.contrib import admin
from .models import Company, Section, Category,Article,SubArticle


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    ordering = ('name',)


@admin.register(Section)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    ordering = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'category')
    ordering = ('title',)


@admin.register(SubArticle)
class SubArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'article')
    ordering = ('title',)
