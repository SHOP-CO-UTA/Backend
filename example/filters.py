from django_filters.filters import CharFilter
from django_filters.rest_framework import FilterSet

from .models import Example


class ExampleFilterSet(FilterSet):
    name = CharFilter(
        field_name="name", lookup_expr="icontains", label="Name"
    )

    class Meta:
        model = Example
        fields = "__all__"
