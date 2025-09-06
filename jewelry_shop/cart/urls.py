from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_page, name="cart_page"),  # Show cart page
    path('get-quantity/', views.get_cart_quantity, name='get_cart_quantity'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('update/', views.update_cart_item, name='update_cart_item'),
    path('batch-update/', views.batch_update_cart, name='batch_update_cart'),
    path('remove/', views.remove_from_cart, name='remove_from_cart'),
]

