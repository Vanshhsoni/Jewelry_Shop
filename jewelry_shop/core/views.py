from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse

from django.shortcuts import render, redirect
from django.urls import reverse

from django.shortcuts import render
from shop.models import Product  # import Product model

def landing_page(request):
    # Fetch only featured products
    featured_products = Product.objects.filter(is_featured=True).order_by('name')
    
    return render(request, "core/landing.html", {
        "featured_products": featured_products
    })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def profile_page(request):
    return render(request, "core/profile.html")