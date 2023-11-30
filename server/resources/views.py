from django.http import HttpRequest, JsonResponse
from rest_framework import viewsets

from resources.models import Resource
from resources.serializers import ResourceSerializer


class ResourceViewSet(viewsets.ViewSet):
    def list(self, request: HttpRequest) -> JsonResponse:
        resources = Resource.objects.all()
        serializer = ResourceSerializer(resources, many=True)
        return JsonResponse({"resources": serializer.data})

    def retrieve(self, request: HttpRequest, pk: int) -> JsonResponse:
        try:
            resource = Resource.objects.get(pk=pk)
            serializer = ResourceSerializer(resource)
            return JsonResponse({"resource": serializer.data})
        except Resource.DoesNotExist:
            return JsonResponse(
                {"error": f"Resource with id {pk} does not exist"},
                status=404,
            )
