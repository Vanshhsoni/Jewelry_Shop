from django.shortcuts import render
from shop.models import *

def category_page(request):
    # Fetch all categories, ordered by name
    categories = Category.objects.all().order_by('name')
    
    # Render the template with the categories context
    return render(request, "shop/category.html", {'categories': categories})

from django.shortcuts import render, get_object_or_404
from shop.models import Category, Product

def item_page(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category).order_by('name')
    return render(request, "shop/item.html", {'products': products, 'category': category})

from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "shop/product_detail.html", {"product": product})
