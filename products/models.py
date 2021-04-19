from uuid import uuid4
from django.db import models
from django.utils.text import slugify


class ParentCategory(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    cat_name = models.CharField(max_length=200)

    def __str__(self):
        return self.cat_name


class Category(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    cat_name = models.CharField(max_length=200)
    parent = models.ForeignKey(
        ParentCategory, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.cat_name


class Tag(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    tag = models.CharField(max_length=200)

    def __str__(self):
        return self.tag


class Color(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    color = models.CharField(max_length=200)

    def __str__(self):
        return self.color


class Product(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    title = models.CharField(max_length=200, null=True)
    price = models.BigIntegerField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    featured = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)
    colors = models.ManyToManyField(Color, blank=True)
    available_in = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='prod/images', blank=True)
    parent_category = models.ForeignKey(
        ParentCategory, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True)
    discount = models.BigIntegerField(
        null=True, blank=True, help_text="Discount percentage for product sales")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
