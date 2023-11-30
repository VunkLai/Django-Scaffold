from django.urls import include, path
from rest_framework import routers

from resources import views

router = routers.SimpleRouter(trailing_slash=False)
router.register("resource", views.ResourceViewSet, basename="resource")

urlpatterns = [
    path("v1/", include(router.urls)),
]
