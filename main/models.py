from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='Companies_logos/')
    founded_date = models.DateField()
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# --------------------------------------------------
class Section(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='Sections_logos/')
    joined_date = models.DateField()
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# --------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='categories_logos/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    section = models.ManyToManyField(Section)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# --------------------------------------------------
class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    section = models.ManyToManyField(Section)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to='articles_logos/')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# --------------------------------------------------
class SubArticle(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='1')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, default='1')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# -----------------------------------------------------

class AgentGroup(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'section')

class Agent(models.Model):
    number = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    phone = models.TextField()
    is_active = models.BooleanField(default=True)
    group = models.ForeignKey(AgentGroup, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
