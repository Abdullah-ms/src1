from import_export import resources
from .models import Company, Section, Category, Article, SubArticle, AgentGroup, Agent


class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company


class SectionResource(resources.ModelResource):
    class Meta:
        model = Section


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class ArticleResource(resources.ModelResource):
    class Meta:
        model = Article


class SubArticleResource(resources.ModelResource):
    class Meta:
        model = SubArticle


class AgentGroupResource(resources.ModelResource):
    class Meta:
        model = AgentGroup


class AgentResource(resources.ModelResource):
    class Meta:
        model = Agent
