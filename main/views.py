from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from main.models import Company, Section, Category, Article, SubArticle
from datetime import datetime
from wisdom.views import daily_wisdom
from django.db.models import Q
from django.utils.html import format_html
import requests
from django.http import JsonResponse


@login_required
def company_list(request):
    wisdom = daily_wisdom()

    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif 12 <= current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    companies = request.user.companies.filter(is_active=True)  # شركات اليوز النشطة فقط

    context = {
        'wisdom': wisdom,
        'greeting': greeting,
        'companies': companies,
    }

    return render(request, 'main/company_list.html', context)

from collections import defaultdict


@login_required
def section_list(request, company_id):
    # الحصول على الشركة باستخدام ال id
    company = get_object_or_404(Company, id=company_id)

    # التحقق من أن الشركة تابعة للمستخدم
    if company not in request.user.companies.all():
        return render(request, 'main/403.html')

    # الحصول على الأقسام المرتبطة بهذه الشركة فقط
    sections = Section.objects.filter(company=company, is_active=True)

    context = {
        'company': company,
        'sections': sections,
    }
    return render(request, 'main/section_list.html', context)


@login_required
def category_list(request, section_id):
    # الحصول على القسم باستخدام ال id
    section = get_object_or_404(Section, id=section_id)

    # التحقق من أن القسم تابع لشركة تابعة للمستخدم
    if section.company not in request.user.companies.all():
        return render(request, 'main/403.html')

    # الحصول على الأصناف المرتبطة بهذا القسم فقط
    categories = Category.objects.filter(section=section, is_active=True)

    context = {
        'section': section,
        'categories': categories,
    }
    return render(request, 'main/category_list.html', context)



@login_required
def article_list(request, category_id, section_id):
    # الحصول على القسم والفئة
    section = get_object_or_404(Section, id=section_id)
    category = get_object_or_404(Category, id=category_id, section=section)
    
        # التحقق من أن القسم تابع لشركة تابعة للمستخدم
    if section.company not in request.user.companies.all():
        return render(request, 'main/403.html')

    # الحصول على جميع المقالات المرتبطة بالفئة والقسم
    articles = Article.objects.filter(category=category, section=section, is_active=True)

    # التحقق إذا كان المستخدم قد اختار مقالة معينة
    article_id = request.GET.get('article_id')
    selected_article = None
    subarticles = None

    if article_id:
        selected_article = get_object_or_404(Article, id=article_id, category=category, section=section)
        subarticles = SubArticle.objects.filter(article=selected_article, section=section, is_active=True)

    context = {
        'section': section,
        'category': category,
        'articles': articles,
        'selected_article': selected_article,
        'subarticles': subarticles,
    }

    return render(request, 'main/articles_and_subarticles.html', context)



@login_required
def search_results(request):
    query = request.GET.get('query')

    # الحصول على الشركات الخاصة بالمستخدم الحالي
    user_companies = request.user.companies.all()

    # التحقق من وجود استعلام وشركات مرتبطة
    if query and user_companies.exists():
        # فلترة المقالات المرتبطة بالأقسام التابعة لشركات المستخدم (مع الأخذ في الاعتبار العلاقة many-to-many)
        articles = Article.objects.filter(
            Q(title__icontains=query),
            section__company__in=user_companies  # التأكد من أن المقالات ضمن أقسام الشركات المرتبطة بالمستخدم
        ).distinct()  # إزالة التكرارات إذا وجد أكثر من علاقة بين المقال والقسم

        # فلترة المقالات الفرعية المرتبطة بمقالات تابعة لشركات المستخدم
        sub_articles = SubArticle.objects.filter(
            (Q(title__icontains=query) | Q(content__icontains=query)),
            section__company__in=user_companies  # التأكد من أن المقالات الفرعية ضمن شركات المستخدم
        ).distinct()  # إزالة التكرارات

        # وظيفة لتحديد النص
        def highlight(text, query):
            highlighted = text.replace(query, f'<span class="highlight">{query}</span>')
            return format_html(highlighted)

        # تحديد النص في العناوين والمحتوى
        for article in articles:
            article.title = highlight(article.title, query)
            for sub_article in article.sub_articles.all():
                sub_article.title = highlight(sub_article.title, query)
                sub_article.content = highlight(sub_article.content, query)

        for sub_article in sub_articles:
            sub_article.title = highlight(sub_article.title, query)
            sub_article.content = highlight(sub_article.content, query)
    else:
        articles = []  # إذا لم تكن هناك نتائج، تفريغ القائمة
        sub_articles = []  # إذا لم تكن هناك نتائج، تفريغ القائمة

    return render(request, 'main/search_results.html', {
        'articles': articles,
        'sub_articles': sub_articles,
        'query': query
    })


@login_required
def subarticle_history_list(request):
    # الحصول على الشركات الخاصة بالمستخدم
    user_companies = request.user.companies.all()

    # الحصول على المقالات الفرعية التابعة لهذه الشركات، مرتبة حسب تاريخ الإضافة أو التحديث
    subarticles = SubArticle.objects.filter(
        section__company__in=user_companies,
        is_active=True
    ).order_by('-updated_at')  # استبدل updated_at بالاسم الصحيح لحقل تاريخ التحديث

    context = {
        'subarticles': subarticles,
    }
    return render(request, 'main/history_list.html', context)


@login_required
def feedback_view(request):
    user_companies = request.user.companies.filter(is_active=True)

    if request.method == 'POST':
        company_id = request.POST.get('company')
        section_id = request.POST.get('section')
        message = request.POST.get('message')

        if not message.strip():
            return render(request, 'feedback.html', {
                'error': 'Message cannot be empty.',
                'companies': user_companies,
            })

        company = Company.objects.get(id=company_id)
        section = Section.objects.get(id=section_id)

        full_message = f"User: {request.user.username}\nCompany: {company.name}\nSection: {section.name}\nMessage: {message}"

        token = "5857300801:AAFjiBN6KOELO9958Dss-_zj640YNXiZyhc"
        chat_id = "507239290"
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": full_message,
        }
        requests.post(url, data=data)

        return redirect('feedback_success')

    return render(request, 'feedback.html', {'companies': user_companies})

@login_required
def get_sections(request, company_id):
    sections = Section.objects.filter(company_id=company_id, is_active=True)
    sections_data = [{'id': section.id, 'name': section.name} for section in sections]
    return JsonResponse({'sections': sections_data})
