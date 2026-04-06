from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Payment
from django.http.response import HttpResponse
import stripe
from django.conf import settings
from django.shortcuts import redirect
from decouple import config
from django.views.decorators.csrf import csrf_exempt


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





@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Payment successful event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        payment_id = session['metadata']['payment_id']

        try:
            payment = Payment.objects.get(id=payment_id)
            payment.status = 'confirmed'
            payment.save()
            print(f"Payment {payment_id} confirmed!")
        except Payment.DoesNotExist:
            print(f"Payment {payment_id} not found!")

    return HttpResponse(status=200)