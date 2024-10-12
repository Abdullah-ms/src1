from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from accounts.forms import CustomUserCreationForm,CustomUserProfileForm, CustomPasswordChangeForm
from main.models import Company, Section, Category,Article,SubArticle

# تغيير باسورد
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('company_list')  # توجيه إلى الصفحة الرئيسية
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')





# تغيير باسورد
@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        profile_form = CustomUserProfileForm(request.POST, instance=user)
        password_form = CustomPasswordChangeForm(user=user, data=request.POST)
        if profile_form.is_valid() and password_form.is_valid():
            profile_form.save()
            password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'تم تحديث كلمة المرور بنجاح.')
            return redirect('profile')
    else:
        profile_form = CustomUserProfileForm(instance=user)
        password_form = CustomPasswordChangeForm(user=user)

    return render(request, 'accounts/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })
