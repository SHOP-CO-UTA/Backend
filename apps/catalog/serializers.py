from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "category_id",
            "name",
            "slug",
            "description",
            "image_url",
            "price",
            "original_price",
            "discount_label",
            "rating",
            "stock",
            "created_at",
            "updated_at",
        ]