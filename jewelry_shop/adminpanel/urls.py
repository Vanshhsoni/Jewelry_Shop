# adminpanel/urls.py
from django.urls import path
from . import views

app_name = "adminpanel"

urlpatterns = [
    # Authentication
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Categories
    path('create-category/', views.create_category, name='create_category'),
    path('category/<int:category_id>/update/', views.update_category, name='update_category'),
    path('category/<int:category_id>/products/', views.category_products, name='category_products'),
    
    # Products
    path('create-product/', views.create_product, name='create_product'),
    path('product/<int:product_id>/', views.get_product, name='get_product'),
    path('product/<int:product_id>/update/', views.update_product, name='update_product'),
    path('product/<int:product_id>/toggle/', views.toggle_product_flag, name='toggle_product_flag'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    
    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
]