from django.urls import include, path
from rest_framework.routers import DefaultRouter
from accounts.api_views import RegisterApiView, LoginApiView, ProfileApiView, VendorApiViewSet
from store.api_views import StoreApiViewSet, CatagoryApiViewSet, ProductApiViewSet, ReviewApiViewSet
from cart.api_views import CartApiViewSet
from order.api_views import CheckoutApiView, OrderApiViewSet, PayoutApiViewSet
from payment.api_views import PaymentApiViewSet
from .api_views import ApiRouteListView

router = DefaultRouter()
router.register('vendors', VendorApiViewSet, basename='api-vendors')
router.register('stores', StoreApiViewSet, basename='api-stores')
router.register('catagories', CatagoryApiViewSet, basename='api-catagories')
router.register('products', ProductApiViewSet, basename='api-products')
router.register('reviews', ReviewApiViewSet, basename='api-reviews')
router.register('carts', CartApiViewSet, basename='api-carts')
router.register('orders', OrderApiViewSet, basename='api-orders')
router.register('payouts', PayoutApiViewSet, basename='api-payouts')
router.register('payments', PaymentApiViewSet, basename='api-payments')

urlpatterns = [
    path('endpoints/', ApiRouteListView.as_view(), name='api_routes'),
    path('register/', RegisterApiView.as_view(), name='api_register'),
    path('login/', LoginApiView.as_view(), name='api_login'),
    path('profile/', ProfileApiView.as_view(), name='api_profile'),
    path('checkout/', CheckoutApiView.as_view(), name='api_checkout'),
    path('', include(router.urls)),
]
