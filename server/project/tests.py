# pylint: disable=redefined-outer-name

import pytest
from project.models import Project, ProjectRole
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
