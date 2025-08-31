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
from cart.models import *
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    initial_quantity = 0
    if request.user.is_authenticated:
        # Get the quantity if the item is already in the user's cart
        cart_item = CartItem.objects.filter(cart__user=request.user, product=product).first()
        if cart_item:
            initial_quantity = cart_item.quantity
            
    context = {
        'product': product,
        'initial_quantity': initial_quantity,
    }
    return render(request, "shop/product_detail.html",context)