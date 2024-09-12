from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('company/<int:company_id>/sections/', views.company_sections, name='company_sections'),
    path('section/<int:section_id>/categories/', views.section_categories, name='section_categories'),
    path('category/<int:category_id>/articles/', views.category_articles, name='category_articles'),
    path('article/<int:article_id>/sub-articles/', views.article_sub_articles, name='article_subarticles'),
]
