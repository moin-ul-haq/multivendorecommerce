from rest_framework import serializers
from .models import Store, Catagory, Product, Review


class StoreSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.name", read_only=True)

    class Meta:
        model = Store
        fields = ["id", "name", "slug", "owner", "owner_name"]
        read_only_fields = ["owner"]


class CatagorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Catagory
        fields = ["id", "name", "slug", "store"]


class ProductSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source="store.name", read_only=True)
    catagory_name = serializers.CharField(source="catagory.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "stock",
            "store",
            "store_name",
            "catagory",
            "catagory_name",
            "slug",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.name", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "product", "user", "user_name", "rating", "review"]
        read_only_fields = ["user"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("rating must be between 1 and 5")
        return value
