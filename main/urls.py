from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.company_list, name='company_list'),  # صفحة الشركات
    path('companies/<int:company_id>/sections/', views.section_list, name='section_list'),
    path('sections/<int:section_id>/categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/<int:section_id>/articles/', views.article_list, name='article_list'),
    #path('articles/<int:article_id>/<int:category_id>/<int:section_id>/subarticles/', views.subarticle_list,name='subarticle_list'),

    path('search/', views.search_results, name='search_results'),
    path('history/', views.subarticle_history_list, name='subarticle_history_list'),
    # path('subarticle/<int:subarticle_id>/', views.subarticle_detail, name='subarticle_detail'),

    # feedback
    path('feedback/', views.feedback_view, name='feedback'),
    path('feedback/success/', TemplateView.as_view(template_name='feedback_success.html'), name='feedback_success'),
    path('get_sections/<int:company_id>/', views.get_sections, name='get_sections'),

]
