from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductPagination(PageNumberPagination):
    page_size = 24
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductPagination
    lookup_field = "id"
    lookup_url_kwarg = "id"
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price", "created_at", "rating", "name", "stock"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = (
            Product.objects
            .prefetch_related(
                "categories",
                "product_categories__category",
                "variants",
            )
            .all()
            .order_by("-created_at")
        )

        # Filter theo category slug (loại SP, vd t-shirts): ?category=t-shirts
        category_slug = self.request.query_params.get("category")
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)

        # Filter theo dress style (cũng là Category slug, vd casual): ?dress_style=casual
        dress_style_slug = self.request.query_params.get("dress_style")
        if dress_style_slug:
            queryset = queryset.filter(categories__slug=dress_style_slug)

        # Filter theo category id: /api/products/?category_id=1
        category_id = self.request.query_params.get("category_id")
        if category_id:
            queryset = queryset.filter(categories__id=category_id)

        min_price = self.request.query_params.get("min_price")
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)

        max_price = self.request.query_params.get("max_price")
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        color = self.request.query_params.get("color")
        if color:
            queryset = queryset.filter(variants__color=color)

        size = self.request.query_params.get("size")
        if size:
            queryset = queryset.filter(variants__size=size)

        # do join M2M / variants nên cần distinct để tránh duplicate
        return queryset.distinct()


class DressStyleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Danh sách các "dress styles" (thực chất là Category được seed sẵn: casual/formal/party/gym).

    Endpoint này phục vụ phần Home -> DressStyle.
    """

    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None  # Trả về array đơn giản (không paginated).

    _DRESS_STYLE_SLUGS = ["casual", "formal", "party", "gym"]

    def get_queryset(self):
        return Category.objects.filter(
            slug__in=self._DRESS_STYLE_SLUGS,
            is_active=True,
        ).order_by("sort_order", "name")


# from django.shortcuts import render
# from rest_framework import viewsets
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.permissions import AllowAny

# from .models import Product
# from .serializers import ProductSerializer

# # Create your views here.
# class ProductPagination(PageNumberPagination):
#     page_size = 24
#     page_size_query_param = "page_size"
#     max_page_size = 100
    

# class ProductViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Product.objects.select_related("category").all().order_by("-created_at")
#     serializer_class = ProductSerializer
#     permission_classes = [AllowAny]
#     pagination_class = ProductPagination
#     ordering_fields = ["price", "created_at", "rating", "name"]