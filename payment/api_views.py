from urllib.parse import urlencode
from django.conf import settings
from decouple import config
import stripe
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Payment
from .serializers import PaymentSerializer
from order.tasks import send_order_status_email


class PaymentApiViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Payment.objects.all()
        return Payment.objects.filter(order__user=self.request.user)

    @action(detail=True, methods=['post'])
    def stripe(self, request, pk=None):
        payment = self.get_object()
        if request.user.role != 'admin' and payment.order.user != request.user:
            return Response({'detail': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)
        stripe.api_key = config('STRIPE_API_KEY')
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(payment.total_amount) * 100,
                        'product_data': {
                            'name': f'Order #{payment.order.id}',
                        },
                    },
                    'quantity': 1,
                }
            ],
            metadata={
                'payment_id': payment.id,
                'order_id': payment.order.id
            },
            mode='payment',
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        return Response({'checkout_url': checkout_session.url}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def paypal(self, request, pk=None):
        payment = self.get_object()
        if request.user.role != 'admin' and payment.order.user != request.user:
            return Response({'detail': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)
        base_url = config('PAYPAL_CHECKOUT_URL', default='https://www.paypal.com/checkoutnow')
        query = urlencode({
            'invoice_id': payment.id,
            'amount': str(payment.total_amount),
            'currency': 'USD',
            'return_url': settings.PAYMENT_SUCCESS_URL,
            'cancel_url': settings.PAYMENT_CANCEL_URL,
        })
        return Response({'checkout_url': f'{base_url}?{query}'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def success(self, request, pk=None):
        payment = self.get_object()
        if request.user.role != 'admin' and payment.order.user != request.user:
            return Response({'detail': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)
        payment.status = 'confirmed'
        payment.save()
        payment.order.status = 'confirmed'
        payment.order.save()
        send_order_status_email.delay(payment.order.user.email, payment.order.id, payment.order.status)
        return Response(PaymentSerializer(payment).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        payment = self.get_object()
        if request.user.role != 'admin' and payment.order.user != request.user:
            return Response({'detail': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)
        payment.status = 'pending'
        payment.save()
        return Response(PaymentSerializer(payment).data, status=status.HTTP_200_OK)
