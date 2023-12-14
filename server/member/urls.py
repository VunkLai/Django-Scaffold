from django.urls import include, path
from rest_framework import routers

from member import views

router = routers.SimpleRouter(trailing_slash=False)
router.register("member", views.MemberViewSet, basename="member")
router.register("organization", views.OrganizationViewSet, basename="organization")

urlpatterns = [
    path("v1/", include(router.urls)),
]
