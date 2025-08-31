from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.conf import settings

from shop.models import Category, Product
from .forms import CategoryForm, ProductForm
from accounts.models import CustomUser  # <- Use your custom user

# -------------------------
# Login / Logout
# -------------------------
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Create admin user if doesn't exist
        user, created = CustomUser.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()

        # Authenticate and login
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('adminpanel:dashboard')
        else:
            return render(request, 'adminpanel/login.html', {'error': 'Invalid credentials or not staff'})

    return render(request, 'adminpanel/login.html')


@login_required
def admin_logout(request):
    logout(request)
    return redirect('adminpanel:login')


# -------------------------
# Staff-only decorator
# -------------------------
def staff_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("Forbidden")
        return view_func(request, *args, **kwargs)
    wrapped.__name__ = view_func.__name__
    return wrapped


# -------------------------
# Dashboard
# -------------------------
@login_required
@staff_required
def dashboard(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'adminpanel/dashboard.html', {'categories': categories})


# -------------------------
# Categories
# -------------------------
@login_required
@staff_required
@require_POST
def create_category(request):
    form = CategoryForm(request.POST, request.FILES)
    if form.is_valid():
        cat = form.save()
        return JsonResponse({'ok': True, 'id': cat.id, 'name': cat.name, 'image_url': cat.image.url})
    return JsonResponse({'ok': False, 'errors': form.errors}, status=400)


@login_required
@staff_required
def category_products(request, category_id):
    cat = get_object_or_404(Category, id=category_id)
    products = cat.products.all().values('id', 'name', 'price', 'is_available', 'is_featured', 'image')
    data = [
        {
            'id': p['id'],
            'name': p['name'],
            'price': str(p['price']),
            'is_available': p['is_available'],
            'is_featured': p['is_featured'],
            'image_url': request.build_absolute_uri('/media/' + str(p['image'])) if p['image'] else ''
        }
        for p in products
    ]
    return JsonResponse({'ok': True, 'category': cat.name, 'products': data})


# -------------------------
# Products
# -------------------------
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


@login_required
@staff_required
@require_POST
def delete_product(request, product_id):
    prod = get_object_or_404(Product, id=product_id)
    prod.delete()
    return JsonResponse({'ok': True})

from django.shortcuts import render
from orders.models import Order

from django.shortcuts import render, redirect, get_object_or_404


def order_list(request):
    orders = Order.objects.prefetch_related('items__product').all().order_by('-created_at')

    # 🔎 Apply filters
    status = request.GET.get("status")
    order_id = request.GET.get("order_id")

    if status:
        orders = orders.filter(status=status)
    if order_id:
        orders = orders.filter(id=order_id)

    return render(request, 'adminpanel/order.html', {'orders': orders})


def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
    return redirect('adminpanel:order_list')
