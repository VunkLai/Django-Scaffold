from http import HTTPStatus

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.models import Organization, User
from authentication.serializers import UserSerializer

# todo: KeyError handler


class MemberViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        return User.objects.filter(organization=self.request.user.organization)

    def list(self, request: HttpRequest) -> JsonResponse:
        users = self.get_queryset()
        if request.user.is_admin:
            serializer = UserSerializer(users, many=True)
            return Response({"users": serializer.data}, status=HTTPStatus.OK)
        return Response({}, status=HTTPStatus.FORBIDDEN)

    def create(self, request: HttpRequest) -> JsonResponse:
        try:
            if request.user.is_admin:
                User.objects.create_user(
                    email=request.data["email"],
                    password=None,
                    organization=request.user.organization,
                )
                return Response({}, status=HTTPStatus.CREATED)
            return Response({}, status=HTTPStatus.FORBIDDEN)
        except IntegrityError:
            return Response({}, status=HTTPStatus.CONFLICT)

    def retrieve(self, request: HttpRequest, pk: int) -> JsonResponse:
        users = self.get_queryset()
        user = get_object_or_404(users, pk=pk)
        if request.user.is_admin or request.user == user:
            serializer = UserSerializer(user)
            return Response({"user": serializer.data}, status=HTTPStatus.OK)
        return Response({}, status=HTTPStatus.FORBIDDEN)

    def update(self, request: HttpRequest, pk: int) -> JsonResponse:
        users = self.get_queryset()
        user = get_object_or_404(users, pk=pk)
        if request.user == user:
            if password := request.data.get("password"):
                user.set_password(password)
            user.save()
            return Response({}, status=HTTPStatus.OK)
        if request.user.role == User.Role.ADMIN:
            if is_active := request.data.get("is_active"):
                user.is_active = is_active
            if role := request.data.get("role"):
                user.role = role
            user.save()
            return Response({}, status=HTTPStatus.OK)
        return Response({}, status=HTTPStatus.FORBIDDEN)

    def destroy(self, request: HttpRequest, pk: int) -> JsonResponse:
        users = self.get_queryset()
        user = get_object_or_404(users, pk=pk)
        user.delete()
        return Response({}, status=HTTPStatus.OK)


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
