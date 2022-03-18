from django.db import models
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.urls import reverse
from PIL import Image
# Create your models here.

User = get_user_model()

class Volunteer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=50, help_text="Volunteer mobile phone")
    image = models.ImageField(upload_to='volunteers/')
    job_role = models.CharField(max_length=150)
    education = models.CharField(max_length=50, help_text="Volunteer educational background")
    social_handle_link = models.URLField(
        max_length=500, null=True, blank=True, 
        help_text="Volunteer social profile e.g. LinkedIn, Instagram or Twitter.")

    def __str__(self) -> str:
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=150, help_text="Name of the event")
    event_date_time = models.DateTimeField()
    thumbnail = models.ImageField(upload_to="events/%Y/%m/%d", null=True, blank=True)
    registration_link = models.URLField(max_length=500)
    event_location = models.CharField(max_length=150, help_text="Where will the events be happening?")
    date_created = models.DateTimeField(auto_now_add=True)
    donations = models.FloatField(default=0, help_text="DOnations made for the event")
    is_active = models.BooleanField(default=True)


    def __str__(self) -> str:
        return self.name


"""
Blog
"""
class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Article(models.Model):
    author = models.ForeignKey(
        User, 
        null=True, 
        on_delete=models.SET_NULL
        )
    title = models.CharField(max_length=240, help_text="Article title")
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        help_text="Select a category that this article belong to."
        )
    featured_image = models.ImageField(upload_to='articles/', null=True, blank=True, help_text="Article image")
    image_credit = models.CharField(max_length=120, null=True, blank=True)
    content = RichTextUploadingField()
    featured = models.BooleanField(default=False)
    date_stamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(
        default='',
        editable=False,
        max_length=120,
    )        

    def __str__(self):
        return f'{self.title}'
        

    class Meta:
        unique_together = ('title', 'slug')
        ordering = ['-id']

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('article_detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
        if self.featured_image:
            img = Image.open(self.featured_image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300,300)
                img.thumbnail(output_size)
                img.save(self.featured_image.path)

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(null=True, blank=True, max_length=120)
    content = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    date_stamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return "{} commented under '{}' on {}".format(self.name, self.article.title, self.date_stamp.date())

