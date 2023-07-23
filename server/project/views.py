from http import HTTPStatus

from django.contrib.auth.models import Permission
from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework import viewsets

from project.models import Member, Project, ProjectRole
from project.serializers import ProjectSerializer


class ProjectViewSet(viewsets.ViewSet):
    def list(self, request: HttpRequest) -> HttpResponse:
        projects = Project.objects.filter(member__user=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return JsonResponse({"projects": serializer.data})

    def retrieve(self, request: HttpRequest, pk: int) -> HttpResponse:
        project = Project.objects.get(pk=pk)
        if project.members.filter(user=request.user).exists():
            serializer = ProjectSerializer(project, many=False)
            return JsonResponse({"project": serializer.data})
        return JsonResponse({"status": "error"}, status=HTTPStatus.FORBIDDEN)

    def create(self, request: HttpRequest) -> HttpResponse:
        # permission = Permission.objects.get(codename="add_project")
        if request.user.has_perm("project.add_project"):
            Project.objects.create_project(
                project_name=request.data["project_name"], owner=request.user
            )
            return JsonResponse({"status": "success"}, status=HTTPStatus.CREATED)
        return JsonResponse({"status": "error"}, status=HTTPStatus.FORBIDDEN)

    def update(self, request: HttpRequest, pk: int) -> HttpResponse:
        project = Project.objects.get(pk=pk)
        member = Member.objects.get(user=request.user, project=project)
        if member.role in [ProjectRole.OWNER, ProjectRole.MAINTAINER]:
            project.name = request.data["project_name"]
            project.save()
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error"}, status=HTTPStatus.FORBIDDEN)

    def destroy(self, request: HttpRequest, pk: int) -> HttpResponse:
        project = Project.objects.get(pk=pk)
        member = Member.objects.get(user=request.user, project=project)
        if member.role == ProjectRole.OWNER:
            project.delete()
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error"}, status=HTTPStatus.FORBIDDEN)
