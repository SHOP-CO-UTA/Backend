from rest_framework import routers
from django.urls import path, include

from .views import ProductViewSet

app_name = "api_catalog"

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")

urlpatterns = [
    path("", include(router.urls)),
]