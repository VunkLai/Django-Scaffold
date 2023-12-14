from http import HTTPStatus

from django.db import IntegrityError
from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from member.models import Member, Organization
from member.serializers import MemberSerializer, OrganizationSerializer


class OrganizationViewSet(ModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Organization.objects.filter(pk=self.request.user.organization)


class MemberViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        return Member.objects.filter(organization=self.request.user.organization)

    def list(self, request: HttpRequest) -> JsonResponse:
        users = self.get_queryset()
        if request.user.is_admin:
            serializer = MemberSerializer(users, many=True)
            return Response({"users": serializer.data}, status=HTTPStatus.OK)
        return Response({}, status=HTTPStatus.FORBIDDEN)

    def create(self, request: HttpRequest) -> JsonResponse:
        try:
            if request.user.is_admin:
                Member.objects.create_user(
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
            serializer = MemberSerializer(user)
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
        if request.user.role == Member.Role.ADMIN:
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
