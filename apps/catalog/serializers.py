from rest_framework import serializers
from .models import Product, Category, ProductCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "parent",
            "name",
            "slug",
            "description",
            "image_url",
            "is_active",
            "sort_order",
            "created_at",
            "updated_at",
        ]


class ProductCategoryWriteSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    is_primary = serializers.BooleanField(default=False)


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_mappings = ProductCategoryWriteSerializer(many=True, write_only=True, required=False)
    primary_category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
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
            "categories",
            "primary_category",
            "category_mappings",
        ]

    def get_primary_category(self, obj):
        # Ưu tiên mapping có is_primary=True, nếu không có thì lấy category đầu tiên
        primary = obj.product_categories.filter(is_primary=True).select_related("category").first()
        if primary:
            return CategorySerializer(primary.category).data

        first_cat = obj.categories.first()
        return CategorySerializer(first_cat).data if first_cat else None

    def create(self, validated_data):
        mappings = validated_data.pop("category_mappings", [])
        product = Product.objects.create(**validated_data)
        self._sync_categories(product, mappings)
        return product

    def update(self, instance, validated_data):
        mappings = validated_data.pop("category_mappings", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if mappings is not None:
            self._sync_categories(instance, mappings)

        return instance

    def _sync_categories(self, product, mappings):
        ProductCategory.objects.filter(product=product).delete()

        created_any_primary = False
        for item in mappings:
            is_primary = bool(item.get("is_primary", False))
            if is_primary:
                created_any_primary = True

            ProductCategory.objects.create(
                product=product,
                category_id=item["category_id"],
                is_primary=is_primary,
            )

        # Nếu client không đánh dấu primary, tự set bản ghi đầu tiên là primary
        if mappings and not created_any_primary:
            first_mapping = ProductCategory.objects.filter(product=product).first()
            if first_mapping:
                first_mapping.is_primary = True
                first_mapping.save(update_fields=["is_primary"])


# from rest_framework import serializers
# from .models import Product, Category


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ["id", "name", "slug"]


# class ProductSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     category_id = serializers.IntegerField(write_only=True)

#     class Meta:
#         model = Product
#         fields = [
#             "id",
#             "category",
#             "category_id",
#             "name",
#             "slug",
#             "description",
#             "image_url",
#             "price",
#             "original_price",
#             "discount_label",
#             "rating",
#             "stock",
#             "created_at",
#             "updated_at",
#         ]