from django.db import models
from django.conf import settings
from shop.models import Product
from django.db.models import Sum, F
class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart_carts'  # 👈 unique related_name
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def total_items(self):
        result = self.items.aggregate(total_quantity=Sum('quantity'))
        return result['total_quantity'] or 0

    def total_price(self):
        result = self.items.aggregate(total=Sum(F('quantity') * F('product__price')))
        return result['total'] or 0.00


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_order_items'  # 👈 unique related_name
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def total_price(self):
        return self.quantity * self.product.price
