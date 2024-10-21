from django.contrib import admin
from .models import Company, Section, Category, Article, SubArticle, Agent, AgentGroup


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ['is_active']
    search_fields = ['name',]
    ordering = ('name',)


@admin.register(Section)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ['company', 'is_active']
    search_fields = ['name',]
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ['section', 'is_active',]
    search_fields = ['name',]
    ordering = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active')
    list_filter = ['section','category', 'is_active',]
    search_fields = ['title',]
    ordering = ('title',)


@admin.register(SubArticle)
class SubArticleAdmin(admin.ModelAdmin):
    list_display = ('title','article','is_active',)
    list_filter = ['section','category','article', 'is_active',]
    search_fields = ['title',]
    ordering = ('title',)


@admin.register(AgentGroup)
class AgentGroupAdmin(admin.ModelAdmin):
    list_display = ('name','is_active')
    list_filter = ['section','is_active',]
    search_fields = ['name',]
    ordering = ('name',)


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone','is_active')
    list_filter = ['section','is_active','group']
    search_fields = ['name', 'phone']
    ordering = ('name',)


admin.site.site_header = "Knowledge base administration"
