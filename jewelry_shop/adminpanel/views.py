from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST

from shop.models import Category, Product
from .forms import CategoryForm, ProductForm
from django.contrib.auth.models import User

# --- Login view
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == "Vanshh_soni" and password == "YouKnowWhoIAm":
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            user = authenticate(request, username=username, password=password)
            if user is None:
                # fallback force login
                user = User.objects.get(username=username)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            else:
                login(request, user)
            return redirect('adminpanel:dashboard')
        return render(request, 'adminpanel/login.html', {'error': 'Invalid credentials'})
    return render(request, 'adminpanel/login.html')


@login_required
def admin_logout(request):
    logout(request)
    return redirect('adminpanel:login')


# staff check decorator
def staff_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("Forbidden")
        return view_func(request, *args, **kwargs)
    wrapped.__name__ = view_func.__name__
    return wrapped


@login_required
@staff_required
def dashboard(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'adminpanel/dashboard.html', {'categories': categories})


# Create category (POST / AJAX)
@login_required
@staff_required
@require_POST
def create_category(request):
    form = CategoryForm(request.POST, request.FILES)
    if form.is_valid():
        cat = form.save()
        return JsonResponse({'ok': True, 'id': cat.id, 'name': cat.name, 'image_url': cat.image.url})
    return JsonResponse({'ok': False, 'errors': form.errors}, status=400)


# List products of a category
@login_required
@staff_required
def category_products(request, category_id):
    cat = get_object_or_404(Category, id=category_id)
    products = cat.products.all().values('id','name','price','is_available','is_featured','image')
    data = []
    for p in products:
        data.append({
            'id': p['id'],
            'name': p['name'],
            'price': str(p['price']),
            'is_available': p['is_available'],
            'is_featured': p['is_featured'],
            'image_url': request.build_absolute_uri('/media/' + str(p['image'])) if p['image'] else ''
        })
    return JsonResponse({'ok': True, 'category': cat.name, 'products': data})


# Create product (POST / AJAX)
@login_required
@staff_required
@require_POST
def create_product(request):
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        product = form.save()
        return JsonResponse({
            'ok': True,
            'product': {
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'is_available': product.is_available,
                'is_featured': product.is_featured,
                'image_url': product.image.url if product.image else ''
            }
        })
    return JsonResponse({'ok': False, 'errors': form.errors}, status=400)


# Toggle availability / featured
@login_required
@staff_required
@require_POST
def toggle_product_flag(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    field = request.POST.get('field')
    if field not in ['is_available', 'is_featured']:
        return JsonResponse({'ok': False, 'error': 'bad field'}, status=400)
    val = request.POST.get('value') == 'true'
    setattr(product, field, val)
    product.save()
    return JsonResponse({'ok': True, 'field': field, 'value': getattr(product, field)})


# Delete product
@login_required
@staff_required
@require_POST
def delete_product(request, product_id):
    prod = get_object_or_404(Product, id=product_id)
    prod.delete()
    return JsonResponse({'ok': True})
