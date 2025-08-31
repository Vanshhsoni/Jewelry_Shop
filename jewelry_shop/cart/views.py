from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.core.exceptions import ValidationError
import logging
from shop.models import Product
from .models import Cart, CartItem

logger = logging.getLogger(__name__)

@login_required
def cart_page(request):
    """Render the cart page"""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart/cart.html", {"cart": cart})

@login_required
@require_http_methods(["POST"])
def add_to_cart(request):
    """Add product to cart or increase quantity"""
    try:
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        
        if not product_id:
            return JsonResponse({"success": False, "error": "Product ID required"})
        
        if quantity <= 0:
            return JsonResponse({"success": False, "error": "Invalid quantity"})

        product = get_object_or_404(Product, id=product_id)
        
        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, 
                product=product,
                defaults={'quantity': 0}
            )

            cart_item.quantity += quantity
            cart_item.save()

            # Refresh cart data from database
            cart.refresh_from_db()
            total_items = cart.total_items()
            total_price = cart.total_price()

        return JsonResponse({
            "success": True,
            "quantity": cart_item.quantity,
            "total_items": total_items,
            "item_total": float(cart_item.total_price()),
            "subtotal": float(total_price),
            "message": f"Added {quantity} {product.name}(s) to cart"
        })

    except ValueError:
        return JsonResponse({"success": False, "error": "Invalid quantity format"})
    except ValidationError as e:
        return JsonResponse({"success": False, "error": str(e)})
    except Exception as e:
        logger.error(f"Error adding to cart: {str(e)}")
        return JsonResponse({"success": False, "error": "Something went wrong"})

@login_required
@require_http_methods(["POST"])
def update_cart_item(request):
    """Increase, decrease or remove item from cart"""
    try:
        product_id = request.POST.get("product_id")
        change = int(request.POST.get("change", 0))
        
        if not product_id:
            return JsonResponse({"success": False, "error": "Product ID required"})

        with transaction.atomic():
            cart = get_object_or_404(Cart, user=request.user)
            cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
            
            old_quantity = cart_item.quantity
            cart_item.quantity += change
            
            removed = False
            item_total = 0
            quantity = 0
            
            if cart_item.quantity <= 0:
                cart_item.delete()
                removed = True
            else:
                cart_item.save()
                quantity = cart_item.quantity
                item_total = float(cart_item.total_price())
            
            # Refresh cart data from database to ensure accuracy
            cart.refresh_from_db()
            subtotal = float(cart.total_price())
            total_items = cart.total_items()

        return JsonResponse({
            "success": True,
            "quantity": quantity,
            "item_total": item_total,
            "subtotal": subtotal,
            "total_items": total_items,
            "removed": removed,
            "message": "Cart updated successfully"
        })

    except ValueError:
        return JsonResponse({"success": False, "error": "Invalid change value"})
    except CartItem.DoesNotExist:
        return JsonResponse({"success": False, "error": "Item not found in cart"})
    except Exception as e:
        logger.error(f"Error updating cart: {str(e)}")
        return JsonResponse({"success": False, "error": "Something went wrong"})

@login_required
def get_cart_count(request):
    """Get current cart item count (for navbar updates)"""
    try:
        cart = Cart.objects.get(user=request.user)
        total_items = cart.total_items()
        return JsonResponse({
            "success": True,
            "total_items": total_items
        })
    except Cart.DoesNotExist:
        return JsonResponse({
            "success": True,
            "total_items": 0
        })
    except Exception as e:
        logger.error(f"Error getting cart count: {str(e)}")
        return JsonResponse({"success": False, "error": "Something went wrong"})

@login_required
@require_http_methods(["POST"])
def clear_cart(request):
    """Clear entire cart"""
    try:
        with transaction.atomic():
            cart = get_object_or_404(Cart, user=request.user)
            cart.items.all().delete()
            
        return JsonResponse({
            "success": True,
            "message": "Cart cleared successfully"
        })
    except Exception as e:
        logger.error(f"Error clearing cart: {str(e)}")
        return JsonResponse({"success": False, "error": "Something went wrong"})

# Optional: View to refresh cart data
@login_required
def refresh_cart(request):
    """Refresh cart data from database"""
    try:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        cart_data = {
            "total_items": cart.total_items(),
            "total_price": float(cart.total_price()),
            "items": []
        }
        
        for item in cart.items.select_related('product').all():
            cart_data["items"].append({
                "id": item.id,
                "product_id": item.product.id,
                "name": item.product.name,
                "price": float(item.product.price),
                "quantity": item.quantity,
                "total": float(item.total_price())
            })
        
        return JsonResponse({
            "success": True,
            "cart": cart_data
        })
    except Exception as e:
        logger.error(f"Error refreshing cart: {str(e)}")
        return JsonResponse({"success": False, "error": "Something went wrong"})