from django.shortcuts import render,get_object_or_404
from .models import Cart,CartItem
from store.models import Product
from django.shortcuts import redirect
from django.views.generic import DetailView

def add_to_cart(request,slug):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product=Product.objects.get(slug=slug)
    cart_item, created=CartItem.objects.get_or_create(cart=cart,product=product,defaults={'quantity': 1, 'unit_price': product.price})
    if not created:
        cart_item.quantity+=1
        cart_item.save()
    return redirect('cart')

def remove_from_cart(request,slug):
    cart=get_object_or_404(Cart,user=request.user)
    product=get_object_or_404(Product,slug=slug)
    cartItem=get_object_or_404(CartItem,cart=cart,product=product)
    cartItem.delete()
    return redirect('cart')

def cart_detail(request):
    cart, created=Cart.objects.get_or_create(user=request.user)
    return render(request,'cart/cart_detail.html',context={'cart':cart})


def increase_quantity(request,slug):
    product=get_object_or_404(Product,slug=slug)
    cart=get_object_or_404(Cart,user=request.user)
    cartitem=get_object_or_404(CartItem,cart=cart,product=product)
    cartitem.quantity+=1
    # print(cartitem.quantity)
    cartitem.save()
    return redirect('cart')


def decrease_quantity(request,slug):
    product=get_object_or_404(Product,slug=slug)
    cart=get_object_or_404(Cart,user=request.user)
    cartitem=get_object_or_404(CartItem,cart=cart,product=product)
    if cartitem.quantity>1:
        cartitem.quantity-=1
    # print(cartitem.quantity)
    cartitem.save()
    return redirect('cart')