from rest_framework import routers

from .views import ExampleViewSet

app_name = "api_example"

router = routers.DefaultRouter()

router.register("", ExampleViewSet)

urlpatterns = []

urlpatterns += router.urls
