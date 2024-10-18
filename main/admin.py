from django.contrib import admin
from .models import Company, Section, Category, Article, SubArticle, Agent, AgentGroup


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


@admin.register(AgentGroup)
class AgentGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'region', 'phone')
    ordering = ('name',)


admin.site.site_header = "Knowledge base administration"
