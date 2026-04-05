from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Payment
from django.http.response import HttpResponse
import stripe
from django.conf import settings
from django.shortcuts import redirect
from decouple import config

class PaymentListView(ListView):
    model=Payment
    context_object_name='payments'
    template_name='payment/payment_list.html'

class PaymentDetailView(DetailView):
    model=Payment
    context_object_name='payment'
    template_name='payment/payment_detail.html'
    slug_url_kwarg='pk'
    slug_field='pk'


def payment_success(request):
    return HttpResponse('Payment Succeded')



def payment_cancel(request):
    return HttpResponse('Something Went Wrong!')


def CreateStripeCheckoutSessionView(request, pk):
    stripe.api_key = config('STRIPE_API_KEY')

    payment = Payment.objects.get(id=pk)
    
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(payment.total_amount) * 100,
                    "product_data": {
                        "name": f"Order #{payment.order.id}",
                    },
                },
                "quantity": 1,
            }
        ],
        metadata={
            "payment_id": payment.id,
            "order_id": payment.order.id
        },
        mode="payment",
        success_url=settings.PAYMENT_SUCCESS_URL,
        cancel_url=settings.PAYMENT_CANCEL_URL,
    )
    
    return redirect(checkout_session.url)