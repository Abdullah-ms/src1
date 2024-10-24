from import_export import resources
from .models import Company, Section, Category, Article, SubArticle, AgentGroup, Agent
from datetime import datetime


class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company


class SectionResource(resources.ModelResource):
    class Meta:
        model = Section


class CategoryResource(resources.ModelResource):
    def dehydrate_created_at(self, category):
        # تحقق من أن الحقل من نوع DateTimeField قبل محاولة إزالة tzinfo
        if isinstance(category.created_at, datetime):
            return category.created_at.replace(tzinfo=None)
        return category.created_at

    class Meta:
        model = Category


class ArticleResource(resources.ModelResource):
    def dehydrate_created_at(self, article):
        # تحقق من أن الحقل من نوع DateTimeField قبل محاولة إزالة tzinfo
        if isinstance(article.created_at, datetime):
            return article.created_at.replace(tzinfo=None)
        return article.created_at

    def dehydrate_updated_at(self, article):
        # تحقق من أن الحقل من نوع DateTimeField قبل محاولة إزالة tzinfo
        if isinstance(article.updated_at, datetime):
            return article.updated_at.replace(tzinfo=None)
        return article.updated_at

    class Meta:
        model = Article


class SubArticleResource(resources.ModelResource):
    def dehydrate_created_at(self, sub_article):
        # تحقق من أن الحقل من نوع DateTimeField قبل محاولة إزالة tzinfo
        if isinstance(sub_article.created_at, datetime):
            return sub_article.created_at.replace(tzinfo=None)
        return sub_article.created_at

    def dehydrate_updated_at(self, sub_article):
        # تحقق من أن الحقل من نوع DateTimeField قبل محاولة إزالة tzinfo
        if isinstance(sub_article.updated_at, datetime):
            return sub_article.updated_at.replace(tzinfo=None)
        return sub_article.updated_at

    class Meta:
        model = SubArticle


class AgentGroupResource(resources.ModelResource):
    class Meta:
        model = AgentGroup


class AgentResource(resources.ModelResource):
    class Meta:
        model = Agent
