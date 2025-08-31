from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="categories/")  # category thumbnail/banner

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="products/")  # main product image
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # ₹9999.99 tak

    def __str__(self):
        return self.name
