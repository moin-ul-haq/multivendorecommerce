from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Store, Catagory, Product, Review
from .serializers import (
    StoreSerializer,
    CatagorySerializer,
    ProductSerializer,
    ReviewSerializer,
)


class StoreApiViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        owner = self.request.query_params.get("owner")
        if owner:
            return Store.objects.filter(owner_id=owner)
        return Store.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CatagoryApiViewSet(viewsets.ModelViewSet):
    serializer_class = CatagorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        store_id = self.request.query_params.get("store")
        if store_id:
            return Catagory.objects.filter(store_id=store_id)
        return Catagory.objects.all()


class ProductApiViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Product.objects.all()
        store_id = self.request.query_params.get("store")
        catagory_id = self.request.query_params.get("catagory")
        if store_id:
            queryset = queryset.filter(store_id=store_id)
        if catagory_id:
            queryset = queryset.filter(catagory_id=catagory_id)
        return queryset


class ReviewApiViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.request.query_params.get("product")
        if product_id:
            return Review.objects.filter(product_id=product_id)
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
