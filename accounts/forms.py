from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
from employee.models import Employee
from django.contrib.auth.forms import PasswordChangeForm

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            employee = Employee.objects.get(hr_name=username)
        except Employee.DoesNotExist:
            raise forms.ValidationError("لا يمكنك إنشاء حساب لأنك غير مسجل بقاعدة البيانات.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        employee = Employee.objects.get(hr_name=self.cleaned_data['username'])
        user.is_active = True  # يتم تفعيل الحساب لاحقاً من قبل الإدارة
        if commit:
            user.save()
            user.companies.set(employee.companies.all())  # تحديث الشركات
            user.role = employee.role  # تحديث الدور
            user.save()
        return user



    # تغيير باسورد
class CustomUserProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True)
    class Meta:
        model = CustomUser
        fields = ('username',)

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Current Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm the new password")
