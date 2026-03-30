from rest_framework import routers
from django.urls import path, include

from .views import ProductViewSet, DressStyleViewSet

app_name = "api_catalog"

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(r"dress-styles", DressStyleViewSet, basename="dress-styles")

urlpatterns = [
    path("", include(router.urls)),
]