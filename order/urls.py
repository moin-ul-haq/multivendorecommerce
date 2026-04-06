from django.urls import path
from .views import check_out,OrderListView,OrderDetailView


urlpatterns = [
    path('checkout/',check_out,name='checkout'),
    path('orders/',OrderListView.as_view(),name='orders'),
    path('order/<int:pk>/',OrderDetailView.as_view(),name='order_detail'),
]
