from django.db import models
from django.utils.text import slugify


class Section(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# -----------------------------------------------------------------
class Shift(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Schedule(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# -----------------------------------------------------------------
class DirectManager(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# -----------------------------------------------------------------
class Status(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# -----------------------------------------------------------------
class Role(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# -----------------------------------------------------------------
class Employee(models.Model):
    full_arabic_name = models.CharField(max_length=200)
    full_english_name = models.CharField(max_length=200)
    hr_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    extention = models.CharField(max_length=10)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True)
    hire_date = models.DateField()
    direct_manager = models.ForeignKey(DirectManager, on_delete=models.SET_NULL, null=True)
    companies = models.ManyToManyField('main.Company')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hr_name
