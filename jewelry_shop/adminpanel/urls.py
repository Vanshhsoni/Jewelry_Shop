# adminpanel/urls.py
from django.urls import path
from . import views

app_name = "adminpanel"

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('create-category/', views.create_category, name='create_category'),
    path('category/<int:category_id>/products/', views.category_products, name='category_products'),
    path('create-product/', views.create_product, name='create_product'),
    path('product/<int:product_id>/toggle/', views.toggle_product_flag, name='toggle_product_flag'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
]
