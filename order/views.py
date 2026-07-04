from django.shortcuts import render, redirect
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from django.views.generic import ListView, DetailView
from django.http.response import HttpResponse


class OrderListView(ListView):
    model = Order
    template_name = "order/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(DetailView):
    model = Order
    pk_url_kwarg = "pk"
    query_pk_and_slug = "pk"
    template_name = "order/order_detail.html"
    context_object_name = "order"


def check_out(request):
    cart = request.user.cart

    for cartitem in list(cart.cartitem.all()):
        if cartitem.quantity > cartitem.product.stock:
            return HttpResponse("Item quantity is greater than Product Stock")
    order = Order.objects.create(
        user=request.user,
        total_amount=request.user.cart.get_total(),
        shipping={"City": "Bahawalpur"},
    )
    print(request.user.cart.get_total())

    for cartitem in list(request.user.cart.cartitem.all()):
        if cartitem.quantity <= cartitem.product.stock:
            OrderItem.objects.create(
                order=order,
                product=cartitem.product,
                quantity=cartitem.quantity,
                unit_price=cartitem.product.price,
                vendor_comission=10,
                product_name=cartitem.product.name,
            )
            product = cartitem.product
            product.stock -= cartitem.quantity
            product.save()
    request.user.cart.clear()
    return redirect("cart")
