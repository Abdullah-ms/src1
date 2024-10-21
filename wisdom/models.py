# wisdom/models.py
from django.db import models

class Wisdom(models.Model):
    text = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    author = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.text
