from django.urls import path
from .views import PaymentListView,payment_success,payment_cancel,CreateStripeCheckoutSessionView,PaymentDetailView

urlpatterns = [
    path('payments/',PaymentListView.as_view(),name='payments'),
    path('payments/<int:pk>',PaymentDetailView.as_view(),name='payment_detail'),
    path('success/',payment_success,name='success'),
    path('cancel/',payment_success,name='success'),
        path(
        "create-checkout-session/<int:pk>/",
        CreateStripeCheckoutSessionView,
        name="create-checkout-session",
    ),
]
