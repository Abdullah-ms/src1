from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # صفحة الشركات
    path('company/<int:company_id>/sections/', views.company_sections, name='company_sections'),  # صفحة الأقسام
    path('section/<int:section_id>/categories/', views.section_categories, name='section_categories'),
    # صفحة الأصناف والمقالات
    path('article/<int:article_id>/sub-articles/', views.article_sub_articles, name='article_subarticles'),
    # صفحة المقالات الفرعية
    path('search/', views.search_results, name='search_results'),

    path('sub-article/<int:sub_article_id>/', views.sub_article_detail, name='sub_article_detail'),
]
