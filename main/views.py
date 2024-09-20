from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.models import Company, Section, Category, Article, SubArticle


@login_required
def dashboard(request):
    """عرض الشركات الخاصة بالمستخدم."""
    companies = request.user.companies.all()  # الشركات الخاصة بالمستخدم
    return render(request, 'main/dashboard.html', {'companies': companies})


@login_required
def company_sections(request, company_id):
    """عرض الأقسام الخاصة بالشركة المختارة."""
    company = get_object_or_404(Company, id=company_id)

    # التحقق من أن الشركة تابعة للمستخدم
    if company not in request.user.companies.all():
        return render(request, 'main/403.html')

    sections = Section.objects.filter(company=company)  # الأقسام الخاصة بالشركة
    return render(request, 'main/company_sections.html', {'company': company, 'sections': sections})


@login_required
def section_categories(request, section_id):
    """عرض الفئات والمقالات الخاصة بالقسم."""
    section = get_object_or_404(Section, id=section_id)

    # التحقق من أن القسم تابع لشركة تابعة للمستخدم
    if section.company not in request.user.companies.all():
        return render(request, 'main/403.html')

    categories = Category.objects.filter(section=section)  # الفئات الخاصة بالقسم
    return render(request, 'main/section_categories.html', {'section': section, 'categories': categories})


@login_required
def article_sub_articles(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    # التحقق من أن المقالة مرتبطة بقسم مرتبط بشركة تابعة للمستخدم
    related_sections = article.category.section.all()  # الفئات قد تكون مرتبطة بعدة أقسام
    user_companies = request.user.companies.all()

    # التحقق من أن القسم المرتبط بالمقالة مرتبط بشركة للمستخدم
    if not any(section.company in user_companies for section in related_sections):
        return render(request, 'main/403.html')

    # عرض المقالات الفرعية إذا كان التحقق ناجحاً
    sub_articles = SubArticle.objects.filter(article=article)
    return render(request, 'main/article_sub_articles.html', {'article': article, 'sub_articles': sub_articles})


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
