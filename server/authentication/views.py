from http import HTTPStatus

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpRequest, JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authentication.models import User
from member.models import Organization

# todo: KeyError handler


@api_view(["POST"])
@swagger_auto_schema(operation_summary="Register")
def sign_up(request: HttpRequest) -> JsonResponse:
    email = request.data["email"]
    password = request.data["password"]
    try:
        organization = Organization.objects.create(name=email)
        User.objects.create_user(
            email=email, password=password, organization=organization
        )
        return Response({}, status=HTTPStatus.CREATED)
    except IntegrityError:
        return Response({}, status=HTTPStatus.CONFLICT)


@api_view(["POST"])
@swagger_auto_schema(operation_summary="Login")
def sign_in(request: HttpRequest) -> JsonResponse:
    email = request.data["email"]
    password = request.data["password"]
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return Response({}, status=HTTPStatus.OK)
    return Response({}, status=HTTPStatus.BAD_REQUEST)


@api_view(["POST"])
@swagger_auto_schema(operation_summary="Logout")
def sign_out(request: HttpRequest) -> JsonResponse:
    logout(request)
    return Response({}, status=HTTPStatus.OK)


@api_view(["POST"])
@swagger_auto_schema(operation_summary="Refresh")
def refresh_token(request: HttpRequest) -> JsonResponse:
    # refresh_token = request.data["refresh_token"]
    return Response({}, status=HTTPStatus.OK)
