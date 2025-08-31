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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile_page(request):
    user = request.user   # This is CustomUser now
    return render(request, "core/profile.html", {
        "user": user,
    })

# core/views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def update_profile_field(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        field = request.POST.get("field")
        value = request.POST.get("value")

        if field in ["phone_number", "address"]:
            setattr(request.user, field, value)
            request.user.save()
            return JsonResponse({"success": True, "field": field, "value": value})

    return JsonResponse({"success": False}, status=400)
