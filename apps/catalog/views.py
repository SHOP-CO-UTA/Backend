from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from .models import Product
from .serializers import ProductSerializer

# Create your views here.
class ProductPagination(PageNumberPagination):
    page_size = 24
    page_size_query_param = "page_size"
    max_page_size = 100
    

# Tại sao sử dụng ReadOnlyModelViewSet thay vì ModelViewSet
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related("category").all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductPagination
    ordering_fields = ["price", "created_at", "rating", "name"]