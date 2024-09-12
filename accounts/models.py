from django.contrib.auth.models import AbstractUser
from django.db import models
from main.models import Company
from employee.models import Role


class CustomUser(AbstractUser):
    # الحقول الإضافية التي تحتاجها
    companies = models.ManyToManyField(Company, blank=True)  # حقل غير ظاهر
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)  # حقل غير ظاهر

    def __str__(self):
        return self.username
