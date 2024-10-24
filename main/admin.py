from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Company, Section, Category, Article, SubArticle, Agent, AgentGroup
from .resources import CompanyResource, SectionResource, CategoryResource, ArticleResource, SubArticleResource, \
    AgentGroupResource, AgentResource


@admin.register(Company)
class CompanyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = CompanyResource
    list_display = ('name', 'is_active')
    list_filter = ['is_active']
    search_fields = ['name', ]
    ordering = ('name',)


@admin.register(Section)
class SectionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = SectionResource
    list_display = ('name', 'is_active')
    list_filter = ['company', 'is_active']
    search_fields = ['name', ]
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = CategoryResource
    list_display = ('name', 'is_active')
    list_filter = ['section', 'is_active', ]
    search_fields = ['name', ]
    ordering = ('name',)


@admin.register(Article)
class ArticleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ArticleResource
    list_display = ('title', 'category', 'is_active')
    list_filter = ['section', 'category', 'is_active', ]
    search_fields = ['title', ]
    ordering = ('title',)


@admin.register(SubArticle)
class SubArticleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = SubArticleResource
    list_display = ('title', 'article', 'is_active',)
    list_filter = ['section', 'category', 'article', 'is_active', ]
    search_fields = ['title', ]
    ordering = ('title',)


@admin.register(AgentGroup)
class AgentGroupAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = AgentGroupResource
    list_display = ('name', 'is_active')
    list_filter = ['section', 'is_active', ]
    search_fields = ['name', ]
    ordering = ('name',)


@admin.register(Agent)
class AgentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = AgentResource
    list_display = ('name', 'phone', 'is_active')
    list_filter = ['section', 'is_active', 'group']
    search_fields = ['name', 'phone']
    ordering = ('name',)


admin.site.site_header = "Knowledge base administration"
