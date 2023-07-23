from __future__ import annotations

from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from user.models import User


class ProjectManager(models.Manager):
    def create_project(self, project_name: str, owner: User) -> Project:
        with transaction.atomic():
            project = Project.objects.create(name=project_name)
            Member.objects.create(project=project, user=owner, role=ProjectRole.OWNER)
        return project


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)

    objects = ProjectManager()


class ProjectRole(models.TextChoices):
    GUEST = "g", _("Guest")
    REPORTER = "r", _("Reporter")
    MAINTAINER = "m", _("Maintainer")
    OWNER = "o", _("Owner")


class Member(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="members",
        related_query_name="member",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="members",
        related_query_name="member",
    )
    role = models.CharField(max_length=1, default=ProjectRole.GUEST)
