from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Order, OrderItem

from .models import Order, OrderItem

from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from cart.models import Cart

import razorpay
from django.conf import settings

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == "POST":
        receiver_name = request.POST.get("receiver_name")
        receiver_phone = request.POST.get("receiver_phone")
        shipping_address = request.POST.get("shipping_address")

        # Razorpay order create
        amount = int(cart.total_price() * 100)  # Razorpay paisa me leta hai
        razorpay_order = razorpay_client.order.create(dict(
            amount=amount,
            currency="INR",
            payment_capture="1"
        ))

        order = Order.objects.create(
            user=request.user,
            receiver_name=receiver_name,
            receiver_phone=receiver_phone,
            shipping_address=shipping_address,
            total_amount=cart.total_price(),
            razorpay_order_id=razorpay_order['id']  # 👈 store order id
        )

        # Cart items → OrderItem
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        context = {
            "order": order,
            "cart": cart,
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "razorpay_order_id": razorpay_order["id"],
            "amount": amount,
            "receiver_name": receiver_name,
            "receiver_phone": receiver_phone,
        }
        return render(request, "orders/payment.html", context)

    return render(request, "orders/checkout.html", {"cart": cart})




@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_success.html", {"order": order})

# orders/views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def order_details_api(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    data = {
        "id": order.id,
        "status": order.get_status_display(),
        "total_amount": str(order.total_amount),
        "items": [
            {
                "name": item.product.name if item.product else "Deleted Product",
                "price": str(item.price),
                "quantity": item.quantity,
                "total": str(item.total_price()),
                "image": item.product.image.url if item.product and item.product.image else "",
            }
            for item in order.items.all()
        ]
    }
    return JsonResponse(data)
