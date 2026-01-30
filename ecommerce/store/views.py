from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem, Order
from django.contrib.auth.decorators import login_required
from .recommender import recommend_products
from .models import UserInteraction


def get_cart(request):
    if not request.session.session_key:
        request.session.save()
    
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

def add_to_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += 1
    item.save()
    return redirect('cart')


def cart_view(request):
    cart = get_cart(request)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'store/cart.html', {'items': items, 'total': total})


def checkout(request):
    cart = get_cart(request)
    items = CartItem.objects.filter(cart=cart)
    if not items.exists():
        return redirect('product_list')
        
    total = sum(item.product.price * item.quantity for item in items)

    if request.user.is_authenticated:
        Order.objects.create(user=request.user, total_price=total)
    else:
        Order.objects.create(session_key=request.session.session_key, total_price=total)
        
    items.delete()
    return render(request, 'store/checkout.html', {'total': total})


def product_list(request):
    products = Product.objects.all()
    recommendations = recommend_products(request)
    
    if request.user.is_authenticated:
        liked_product_ids = UserInteraction.objects.filter(
            user=request.user, liked=True
        ).values_list('product_id', flat=True)
    else:
        liked_product_ids = UserInteraction.objects.filter(
            session_key=request.session.session_key, liked=True
        ).values_list('product_id', flat=True)

    return render(request, 'store/products.html', {
        'products': products,
        'recommendations': recommendations,
        'liked_product_ids': liked_product_ids
    })

def like_product(request, product_id):
    if not request.session.session_key:
        request.session.save()
        
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        interaction, created = UserInteraction.objects.get_or_create(
            user=request.user,
            product=product,
        )
    else:
        interaction, created = UserInteraction.objects.get_or_create(
            session_key=request.session.session_key,
            product=product,
        )
    
    if not created:
        interaction.delete()
    else:
        interaction.liked = True
        interaction.save()
        
    return redirect(request.META.get('HTTP_REFERER', '/'))

def liked_products(request):
    if request.user.is_authenticated:
        interactions = UserInteraction.objects.filter(user=request.user, liked=True)
    else:
        interactions = UserInteraction.objects.filter(session_key=request.session.session_key, liked=True)
        
    liked_products = [i.product for i in interactions]
    return render(request, 'store/like.html', {'liked_products': liked_products})
