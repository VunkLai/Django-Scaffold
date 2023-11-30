from http import HTTPStatus

import pytest
from resources.models import Resource
from resources.serializers import ResourceSerializer


@pytest.mark.django_db
def test_urls(client):
    # CASE 1: resource list url
    response = client.get("/api/resources/v1/resource")
    assert response.status_code == 200

    # CASE 2: resource get url
    response = client.get("/api/resources/v1/resource/1")
    assert response.status_code == 404

    resource = Resource.objects.create(name="worker", amount=9527)
    response = client.get(f"/api/resources/v1/resource/{resource.pk}")
    assert response.status_code == 200


@pytest.mark.django_db
def test_resource_list_view(client):
    response = client.get("/api/resources/v1/resource")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"resources": []}


@pytest.mark.django_db
def test_resource_retrieve_view(client):
    # CASE 1: resource does not exist
    response = client.get("/api/resources/v1/resource/1")
    assert response.status_code == HTTPStatus.NOT_FOUND

    # CASE 2: resource exists and the view returns a serialized result
    resource = Resource.objects.create(name="worker", amount=9527)
    serializer = ResourceSerializer(resource)

    response = client.get(f"/api/resources/v1/resource/{resource.pk}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"resource": serializer.data}


@pytest.mark.django_db
def test_resource_model_serializer():
    Resource.objects.create(name="worker", amount=9527)
    Resource.objects.create(name="worker", amount=9527)

    # CASE 1: serialize an object
    obj = Resource.objects.first()
    serializer = ResourceSerializer(obj)
    assert serializer.data == {"name": obj.name, "amount": obj.amount, "id": obj.id}

    # CASE 2: serialize a queryset
    queryset = Resource.objects.all()
    serializer = ResourceSerializer(queryset, many=True)
    assert len(serializer.data) == queryset.count()
