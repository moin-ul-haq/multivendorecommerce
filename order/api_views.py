from decimal import Decimal
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from cart.models import Cart
from .models import Order, OrderItem, Payout
from .serializers import OrderSerializer, PayoutSerializer
from .tasks import send_order_status_email


class CheckoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        if cart.is_empty():
            return Response(
                {"detail": "cart is empty"}, status=status.HTTP_400_BAD_REQUEST
            )
        shipping = request.data.get("shipping", {"City": "Bahawalpur"})
        order = Order.objects.create(
            user=request.user, total_amount=cart.get_total(), shipping=shipping
        )
        for cart_item in list(cart.cartitem.all()):
            if cart_item.quantity <= cart_item.product.stock:
                sub_total = Decimal(str(cart_item.product.price)) * Decimal(
                    str(cart_item.quantity)
                )
                admin_comission = (sub_total * Decimal("0.10")).quantize(
                    Decimal("0.01")
                )
                order_item = OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.product.price,
                    vendor_comission=admin_comission,
                    product_name=cart_item.product.name,
                )
                Payout.objects.create(
                    owner=cart_item.product.store.owner,
                    order_item=order_item,
                    amount=(sub_total - admin_comission),
                    admin_comission=admin_comission,
                )
                product = cart_item.product
                product.stock -= cart_item.quantity
                product.save()
        cart.clear()
        send_order_status_email.delay(request.user.email, order.id, order.status)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderApiViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @action(detail=True, methods=["patch"])
    def status(self, request, pk=None):
        order = self.get_object()
        status_value = request.data.get("status")
        if not status_value:
            return Response(
                {"detail": "status required"}, status=status.HTTP_400_BAD_REQUEST
            )
        order.status = status_value
        order.save()
        send_order_status_email.delay(order.user.email, order.id, order.status)
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)


class PayoutApiViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PayoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == "admin":
            return Payout.objects.all()
        return Payout.objects.filter(owner=self.request.user)

    @action(detail=True, methods=["patch"])
    def status(self, request, pk=None):
        payout = self.get_object()
        if self.request.user.role != "admin":
            return Response(
                {"detail": "only admin can update payout"},
                status=status.HTTP_403_FORBIDDEN,
            )
        status_value = request.data.get("status")
        if status_value:
            payout.status = status_value
            payout.save()
        return Response(PayoutSerializer(payout).data, status=status.HTTP_200_OK)
