from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Catagory
from .models import Store


class StoreListView(ListView):
    model = Store
    context_object_name = "stores"
    template_name = "store/store_list.html"


class StoreDetailView(DetailView):
    model = Store
    context_object_name = "store"
    template_name = "store/store_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "store/product_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class CatagoryListView(ListView):
    model = Catagory
    context_object_name = "catagories"
    template_name = "catagory/catagory_list.html"


class CatagoryDetailView(DetailView):
    model = Catagory
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "catagory"
    template_name = "catagory/catagory_detail.html"


class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "store/product_list.html"
