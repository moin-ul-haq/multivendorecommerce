from django.urls import path 
from .views import StoreListView, StoreDetailView, ProductDetailView, CatagoryListView, CatagoryDetailView, ProductListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='products'),
    path('store/', StoreListView.as_view(), name='store'),
    path('store/<slug:slug>/', StoreDetailView.as_view(), name='store_detail'),
    path('store/<slug:store_slug>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('catagory/', CatagoryListView.as_view(), name='catagory'),
    path('catagory/<slug:slug>/', CatagoryDetailView.as_view(), name='catagory_detail'),
]