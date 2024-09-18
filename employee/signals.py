from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee
from accounts.models import CustomUser

@receiver(post_save, sender=Employee)
def update_user_from_employee(sender, instance, **kwargs):
    print(f"Updating user from employee: {instance.hr_name}")  # تحقق من أنه يتم استدعاء الإشارة
    try:
        user = CustomUser.objects.get(username=instance.hr_name)
        user.companies.set(instance.companies.all())  # تحديث الشركات
        user.role = instance.role  # تحديث الدور
        user.save()
        print(f"User updated: {user.username}")  # تحقق من التحديث
    except CustomUser.DoesNotExist:
        print(f"User not found for hr_name: {instance.hr_name}")  # تحقق إذا لم يتم العثور على المستخدم
