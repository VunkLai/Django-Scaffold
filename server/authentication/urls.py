from django.urls import include, path

from authentication import views

v1_patterns = [
    path("sign_up", views.sign_up),
    path("sign_in", views.sign_in),
    path("sign_out", views.sign_out),
    path("refresh", views.refresh_token),
]

urlpatterns = [
    path("v1/", include(v1_patterns)),
]
