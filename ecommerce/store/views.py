from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem, Order
# from django.contrib.auth.decorators import login_required
from .recommender import recommend_products
from .models import UserInteraction


# @login_required
def add_to_cart(request, product_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += 1
    item.save()

    return redirect('cart')


# @login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'store/cart.html', {'items': items, 'total': total})


# @login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)

    Order.objects.create(user=request.user, total_price=total)
    items.delete()

    return render(request, 'store/checkout.html', {'total': total})


def product_list(request):
    products = Product.objects.all()
    recommendations = None
    liked_product_ids = []

    if request.user.is_authenticated:
        recommendations = recommend_products(request.user)
        liked_product_ids = UserInteraction.objects.filter(user=request.user, liked=True).values_list('product_id', flat=True)

    return render(request, 'store/products.html', {
        'products': products,
        'recommendations': recommendations,
        'liked_product_ids': liked_product_ids
    })

# @login_required
def like_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    interaction, created = UserInteraction.objects.get_or_create(
        user=request.user,
        product=product,
    )
    
    if not created:
        # Toggle liked status or just delete the interaction if it exists
        # If we only use UserInteraction for likes, deleting it is cleaner
        interaction.delete()
    else:
        interaction.liked = True
        interaction.save()
        
    return redirect(request.META.get('HTTP_REFERER', '/'))

# @login_required
def liked_products(request):
    interactions = UserInteraction.objects.filter(user=request.user, liked=True)
    liked_products = [i.product for i in interactions]
    return render(request, 'store/like.html', {'liked_products': liked_products})