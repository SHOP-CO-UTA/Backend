from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from .models import Product
from .serializers import ProductSerializer


class ProductPagination(PageNumberPagination):
    page_size = 24
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price", "created_at", "rating", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = (
            Product.objects
            .prefetch_related("categories", "product_categories__category")
            .all()
            .order_by("-created_at")
        )

        # Filter theo category slug: /api/products/?category=casual
        category_slug = self.request.query_params.get("category")
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)

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

        # do join M2M nên cần distinct để tránh duplicate
        return queryset.distinct()


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