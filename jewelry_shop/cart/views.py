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
# cart/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import Cart, CartItem
from shop.models import Product

@login_required
@require_POST
def get_cart_quantity(request):
    """Get current quantity of a product in cart - optimized single query"""
    product_id = request.POST.get('product_id')
    
    if not product_id:
        return JsonResponse({'error': 'Product ID required'}, status=400)
    
    try:
        # Single optimized query with select_related
        cart_item = CartItem.objects.select_related('cart', 'product').get(
            cart__user=request.user, 
            product_id=product_id
        )
        return JsonResponse({'quantity': cart_item.quantity})
    except CartItem.DoesNotExist:
        return JsonResponse({'quantity': 0})
    except Exception as e:
        return JsonResponse({'error': 'Failed to get quantity'}, status=500)


@login_required
@require_POST
def add_to_cart(request):
    """Add product to cart - optimized with get_or_create"""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    if not product_id:
        return JsonResponse({'error': 'Product ID required'}, status=400)
    
    try:
        product = get_object_or_404(Product, id=product_id, is_available=True)
        
        with transaction.atomic():
            # Get or create cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Get or create cart item - this is much faster than separate queries
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not item_created:
                cart_item.quantity += quantity
                cart_item.save(update_fields=['quantity'])
        
        return JsonResponse({
            'success': True,
            'quantity': cart_item.quantity,
            'total_items': cart.total_items()
        })
        
    except Exception as e:
        return JsonResponse({'error': 'Failed to add to cart'}, status=500)


@login_required
@require_POST  
def update_cart_item(request):
    """Update cart item quantity - optimized batch processing"""
    product_id = request.POST.get('product_id')
    change = int(request.POST.get('change', 0))
    
    if not product_id or change == 0:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)
    
    try:
        with transaction.atomic():
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.select_for_update().get(
                cart=cart, 
                product_id=product_id
            )
            
            new_quantity = max(0, cart_item.quantity + change)
            
            if new_quantity <= 0:
                cart_item.delete()
                return JsonResponse({
                    'success': True,
                    'quantity': 0,
                    'total_items': cart.total_items()
                })
            else:
                cart_item.quantity = new_quantity
                cart_item.save(update_fields=['quantity'])
                
                return JsonResponse({
                    'success': True,
                    'quantity': cart_item.quantity,
                    'total_items': cart.total_items()
                })
                
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return JsonResponse({'error': 'Cart item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': 'Failed to update cart'}, status=500)


@login_required
@require_POST
def remove_from_cart(request):
    """Remove item completely from cart"""
    product_id = request.POST.get('product_id')
    
    if not product_id:
        return JsonResponse({'error': 'Product ID required'}, status=400)
    
    try:
        with transaction.atomic():
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            
            return JsonResponse({
                'success': True,
                'total_items': cart.total_items(),
                'total_price': float(cart.total_price())
            })
            
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return JsonResponse({'error': 'Cart item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': 'Failed to remove item'}, status=500)

# cart/views.py

@login_required
@require_POST
def batch_update_cart(request):
    """Handle multiple cart updates in one request - for rapid clicking"""
    product_id = request.POST.get('product_id')
    total_change = int(request.POST.get('total_change', 0))

    if not product_id: # total_change can be 0 if the item is new
        return JsonResponse({'error': 'Invalid parameters'}, status=400)
    
    try:
        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart_item = CartItem.objects.select_for_update().filter(cart=cart, product_id=product_id).first()

            if cart_item:
                new_quantity = max(0, cart_item.quantity + total_change)
                if new_quantity <= 0:
                    cart_item.delete()
                    cart_item = None # Item is gone
                else:
                    cart_item.quantity = new_quantity
                    cart_item.save(update_fields=['quantity'])
            elif total_change > 0:
                # Item doesn't exist, create it
                product = get_object_or_404(Product, id=product_id, is_available=True)
                cart_item = CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=total_change
                )

        # Recalculate totals after transaction
        current_quantity = cart_item.quantity if cart_item else 0
        total_items = cart.total_items()
        total_price = float(cart.total_price()) # ⭐ ADDED: Calculate total price

        return JsonResponse({
            'success': True,
            'quantity': current_quantity,
            'total_items': total_items,
            'total_price': total_price # ⭐ ADDED: Return total price
        })
            
    except Exception as e:
        logger.error(f"Error in batch_update_cart: {e}")
        return JsonResponse({'success': False, 'error': 'Failed to update cart'}, status=500)