from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.models import Company, Section, Category, Article, SubArticle


# عرض الشركات الخاصة بالمستخدم
@login_required
def company_list(request):
    companies = request.user.companies.all()  # الشركات الخاصة بالمستخدم
    return render(request, 'main/company_list.html', {'companies': companies})


# عرض الأقسام الخاصة بالشركة
def section_list(request, company_id):
    # الحصول على الشركة باستخدام المعرّف
    company = get_object_or_404(Company, id=company_id)

    # الحصول على الأقسام المرتبطة بهذه الشركة فقط
    sections = Section.objects.filter(company=company)

    context = {
        'company': company,
        'sections': sections,
    }
    return render(request, 'main/section_list.html', context)


# عرض الأصناف الخاصة بالقسم
from django.shortcuts import render, get_object_or_404
from .models import Section, Category

def category_list(request, section_id):
    # الحصول على القسم باستخدام المعرّف
    section = get_object_or_404(Section, id=section_id)

    # الحصول على الأصناف المرتبطة بهذا القسم فقط
    categories = Category.objects.filter(section=section)

    context = {
        'section': section,
        'categories': categories,
    }
    return render(request, 'main/category_list.html', context)


# عرض المقالات الخاصة بالصنف والقسم
def article_list(request, category_id, section_id):
    # الحصول على القسم باستخدام المعرّف
    section = get_object_or_404(Section, id=section_id)

    # الحصول على الفئة المرتبطة بهذا القسم
    category = get_object_or_404(Category, id=category_id, section=section)

    # الحصول على المقالات المرتبطة بهذه الفئة والقسم
    articles = Article.objects.filter(category=category, section=section)

    context = {
        'section': section,
        'category': category,
        'articles': articles,
    }
    return render(request, 'main/article_list.html', context)


# عرض المقالات الفرعية الخاصة بالمقالة والصنف والقسم
def subarticle_list(request, article_id, category_id, section_id):
    # الحصول على القسم
    section = get_object_or_404(Section, id=section_id)

    # الحصول على المقالة باستخدام المعرّف
    article = get_object_or_404(Article, id=article_id, category_id=category_id)

    # الحصول على المقالات الفرعية المرتبطة بهذه المقالة والتي تنتمي إلى القسم المحدد
    subarticles = SubArticle.objects.filter(article=article, section=section)

    context = {
        'article': article,
        'subarticles': subarticles,
        'section': section,
    }
    return render(request, 'main/subarticle_list.html', context)

@login_required
def search_results(request):
    query = request.GET.get('query')
    if query:
        articles = Article.objects.filter(title__icontains=query)
        sub_articles = SubArticle.objects.filter(title__icontains=query)
    else:
        articles = []
        sub_articles = []

    return render(request, 'main/search_results.html',
                  {'articles': articles, 'sub_articles': sub_articles, 'query': query})


def sub_article_detail(request, sub_article_id):
    sub_article = get_object_or_404(SubArticle, id=sub_article_id)
    article = sub_article.article
    return render(request, 'main/sub_article_detail.html', {'article': article, 'sub_article': sub_article})
