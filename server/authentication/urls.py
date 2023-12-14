from django.urls import include, path
from rest_framework import routers

from authentication import views

router = routers.SimpleRouter(trailing_slash=False)
router.register("member", views.MemberViewSet, basename="member")

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/sign_up", views.sign_up),
    path("v1/sign_in", views.sign_in),
    path("v1/sign_out", views.sign_out),
    path("v1/refresh", views.refresh_token),
]
