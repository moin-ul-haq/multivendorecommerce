from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart, CartItem
from .serializers import CartSerializer
from store.models import Product


class CartApiViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def list(self, request):
        cart = self.get_object()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def me(self, request):
        cart = self.get_object()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='add/(?P<slug>[^/.]+)')
    def add(self, request, slug=None):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, slug=slug)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1, 'unit_price': product.price}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='remove/(?P<slug>[^/.]+)')
    def remove(self, request, slug=None):
        cart = get_object_or_404(Cart, user=request.user)
        product = get_object_or_404(Product, slug=slug)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        cart_item.delete()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='increase/(?P<slug>[^/.]+)')
    def increase(self, request, slug=None):
        cart = get_object_or_404(Cart, user=request.user)
        product = get_object_or_404(Product, slug=slug)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='decrease/(?P<slug>[^/.]+)')
    def decrease(self, request, slug=None):
        cart = get_object_or_404(Cart, user=request.user)
        product = get_object_or_404(Product, slug=slug)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def clear(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.clear()
        return Response({'detail': 'cart cleared'}, status=status.HTTP_200_OK)
