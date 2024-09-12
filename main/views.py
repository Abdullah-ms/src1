from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.models import Company, Section, Category, Article, SubArticle


@login_required
def dashboard(request):
    companies = request.user.companies.all()
    return render(request, 'main/dashboard.html', {'companies': companies})


@login_required
def company_sections(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    sections = Section.objects.filter(company=company)
    return render(request, 'main/company_sections.html', {'company': company, 'sections': sections})


@login_required
def section_categories(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    categories = Category.objects.filter(section=section)
    return render(request, 'main/section_categories.html', {'section': section, 'categories': categories})


@login_required
def category_articles(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    articles = Article.objects.filter(category=category)
    return render(request, 'main/category_articles.html', {'category': category, 'articles': articles})


@login_required
def article_sub_articles(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    sub_articles = SubArticle.objects.filter(article=article)
    return render(request, 'main/article_sub_articles.html', {'article': article, 'sub_articles': sub_articles})
