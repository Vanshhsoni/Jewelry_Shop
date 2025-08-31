from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_page, name="cart_page"),  # Show cart page
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),  # AJAX add/increase
    path("update-cart-item/", views.update_cart_item, name="update_cart_item"),  # AJAX increase/decrease/remove
    path("get-cart-count/", views.get_cart_count, name="get_cart_count"),  # Get cart count for navbar
    path("clear-cart/", views.clear_cart, name="clear_cart"),  # Clear entire cart
    path("refresh-cart/", views.refresh_cart, name="refresh_cart"),  # Refresh cart data
]