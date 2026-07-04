from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_slug = serializers.CharField(source="product.slug", read_only=True)
    sub_total = serializers.DecimalField(
        source="get_sub_total", max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_slug",
            "quantity",
            "unit_price",
            "sub_total",
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source="cartitem", many=True, read_only=True)
    total = serializers.DecimalField(
        source="get_total", max_digits=12, decimal_places=2, read_only=True
    )
    items_count = serializers.IntegerField(source="get_items_count", read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "is_active", "items", "total", "items_count"]
