from rest_framework import serializers
from .models import Order, OrderItem, Payout


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "unit_price",
            "vendor_comission",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment_id = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "total_amount",
            "shipping",
            "items",
            "payment_id",
            "payment_status",
        ]
        read_only_fields = ["user", "total_amount"]

    def get_payment_id(self, obj):
        payment = obj.payments.first()
        if payment:
            return payment.id
        return None

    def get_payment_status(self, obj):
        payment = obj.payments.first()
        if payment:
            return payment.status
        return None


class PayoutSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.name", read_only=True)

    class Meta:
        model = Payout
        fields = [
            "id",
            "owner",
            "owner_name",
            "order_item",
            "amount",
            "admin_comission",
            "status",
        ]
