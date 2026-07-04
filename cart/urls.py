from django.urls import path
from .views import (
    cart_detail,
    add_to_cart,
    remove_from_cart,
    increase_quantity,
    decrease_quantity,
)

urlpatterns = [
    path("cart/", cart_detail, name="cart"),
    path("cart/add/<slug:slug>/", add_to_cart, name="add_to_cart"),
    path("cart/remove/<slug:slug>/", remove_from_cart, name="remove_from_cart"),
    path("cart/increase/<slug:slug>/", increase_quantity, name="increase_quantity"),
    path("cart/decrease/<slug:slug>/", decrease_quantity, name="decrease_quantity"),
]
