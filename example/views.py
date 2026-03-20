from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .filters import ExampleFilterSet
from .models import Example
from .serializers import ExampleSerializer


# Create your views here.
class ExampleViewSet(viewsets.ModelViewSet):
    queryset = Example.objects.all()
    serializer_class = ExampleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filterset_class = ExampleFilterSet
    ordering_fields = ["__all__"]