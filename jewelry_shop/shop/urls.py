from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("category/", views.category_page, name="category"),
    path("item/<int:category_id>/", views.item_page, name="item"),  # category listing
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),  # single product page# In your cart urls.py
]
