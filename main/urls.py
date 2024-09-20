from django.urls import path
from . import views

urlpatterns = [
    path('', views.company_list, name='company_list'),  # صفحة الشركات
    path('companies/<int:company_id>/sections/', views.section_list, name='section_list'),
    path('sections/<int:section_id>/categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/<int:section_id>/articles/', views.article_list, name='article_list'),
    path('articles/<int:article_id>/<int:category_id>/<int:section_id>/subarticles/', views.subarticle_list, name='subarticle_list'),

    path('search/', views.search_results, name='search_results'),

    path('sub-article/<int:sub_article_id>/', views.sub_article_detail, name='sub_article_detail'),
]
