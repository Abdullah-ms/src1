from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Employee
from accounts.models import CustomUser

@receiver(m2m_changed, sender=Employee.companies.through)
def update_user_companies(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        print(f"Updating user companies for: {instance.hr_name}")
        try:
            user = CustomUser.objects.get(username=instance.hr_name)
            user.companies.set(instance.companies.all())  # Update companies
            user.save()
            print(f"User companies updated: {user.username}")
        except CustomUser.DoesNotExist:
            print(f"User not found for hr_name: {instance.hr_name}")
