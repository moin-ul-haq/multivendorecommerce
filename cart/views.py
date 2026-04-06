from django.shortcuts import render,get_object_or_404
from .models import Cart,CartItem
from store.models import Product
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.http.response import HttpResponse

def add_to_cart(request,slug):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product=Product.objects.get(slug=slug)
    if product.stock>=1:
        cart_item, created=CartItem.objects.get_or_create(cart=cart,product=product,defaults={'quantity': 1, 'unit_price': product.price})
        if not created:
            if cart_item.quantity<cart_item.product.stock:
                cart_item.quantity+=1
                cart_item.save()
        return redirect('cart')
    return HttpResponse("Product Out of stock!!")

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
    if product.stock>cartitem.quantity:
        cartitem.quantity+=1
    # print(cartitem.quantity)
        cartitem.save()
        return redirect('cart')
    return HttpResponse('Product out of stock')


def decrease_quantity(request,slug):
    product=get_object_or_404(Product,slug=slug)
    cart=get_object_or_404(Cart,user=request.user)
    cartitem=get_object_or_404(CartItem,cart=cart,product=product)
    if cartitem.quantity>1:
        cartitem.quantity-=1
    # print(cartitem.quantity)
    cartitem.save()
    return redirect('cart')