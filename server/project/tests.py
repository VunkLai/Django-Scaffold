# pylint: disable=redefined-outer-name
from http import HTTPStatus

from django.contrib.auth.models import Permission
from django.test import Client

import pytest
from project.models import Member, Project, ProjectRole
from user.models import User


@pytest.fixture(scope="function")
def user():
    user = User.objects.create_user(username="username", password="password")
    yield user
    user.delete()


@pytest.mark.django_db
def test_project(user: User) -> None:
    project = Project.objects.create_project(project_name="first_project", owner=user)

    assert project.name == "first_project"
    assert project.members
    for member in project.members.all():
        assert member.role == ProjectRole.OWNER


@pytest.mark.django_db
def test_api_create_project(client: Client, user: User) -> None:
    client.force_login(user)
    response = client.post(
        "/v1/project",
        content_type="application/json",
        data={"project_name": "first_project"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN

    permission = Permission.objects.get(codename="add_project")
    user.user_permissions.add(permission)

    response = client.post(
        "/v1/project",
        content_type="application/json",
        data={"project_name": "first_project"},
    )
    assert response.status_code == HTTPStatus.CREATED

    projects = Project.objects.filter(name="first_project")
    assert projects.exists()

    project = projects.get()
    members = project.members.filter(user=user)
    assert members.exists()


@pytest.mark.django_db
def test_api_retrieve_project(client: Client, user: User) -> None:
    project = Project.objects.create_project(project_name="first_project", owner=user)

    client.force_login(user)
    response = client.get(
        f"/v1/project/{project.id}",
    )
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data["project"]["name"] == project.name

    response = client.get(
        "/v1/project",
    )
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data["projects"][0]["name"] == project.name


@pytest.mark.django_db
def test_api_update_project(client: Client, user: User) -> None:
    project = Project.objects.create_project(project_name="first_project", owner=user)

    client.force_login(user)
    response = client.put(
        f"/v1/project/{project.id}",
        content_type="application/json",
        data={"project_name": "second_project"},
    )
    assert response.status_code == HTTPStatus.OK

    projects = Project.objects.filter(name="second_project")
    assert projects.exists()


@pytest.mark.django_db
def test_api_update_project(client: Client, user: User) -> None:
    project = Project.objects.create_project(project_name="first_project", owner=user)

    client.force_login(user)
    response = client.delete(
        f"/v1/project/{project.id}",
        content_type="application/json",
    )
    assert response.status_code == HTTPStatus.OK

    projects = Project.objects.filter(name="first_project")
    assert not projects.exists()
