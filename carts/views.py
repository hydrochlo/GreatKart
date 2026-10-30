from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        if cart_items:
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
                tax = (2 * total)/100
                grand_total = total + tax
        else:
            tax = 0
            grand_total = 0
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'quantitly': quantity,
        'cart_items': cart_items,
        'grand_total': grand_total,
        'tax': tax,
    }
        
    return render(request, 'store/cart.html', context)

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()

    return cart
    
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id) # Get the product
    product_variation = []
    
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                variation = Variation.objects.get(variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # Get the cart using the cart_id present in the session
        
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        
        cart.save()
        
    is_cart_item_exit = CartItem.objects.filter(product=product, cart=cart).exists()
    
    if is_cart_item_exit:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        # existing variation -> database
        # current variation -> product_variation        
        # item_id -> database
        existing_variation_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            existing_variation_list.append(list(existing_variation))
            id.append(item.id)
        
        if product_variation in existing_variation_list:
            # increate the cart item quantity
            idx = existing_variation_list.index(product_variation)
            item_id = id[idx]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')
    
def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)    
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1;
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')