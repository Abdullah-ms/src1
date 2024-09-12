from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser
from employee.models import Employee

@receiver(post_save, sender=CustomUser)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            employee = Employee.objects.get(hr_name=instance.username)
            instance.companies.set(employee.companies.all())
            instance.role = employee.role
            instance.save()
        except Employee.DoesNotExist:
            pass
