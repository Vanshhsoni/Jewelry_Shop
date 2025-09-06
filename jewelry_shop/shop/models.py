# From cloudinary.models import CloudinaryField  # This is for the `cloudinary` library
from cloudinary_storage.models import CloudinaryField  # This is for the `django-cloudinary-storage` library

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = CloudinaryField('image')  # Replaced ImageField with CloudinaryField

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    image = CloudinaryField('image')  # Replaced ImageField with CloudinaryField
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
