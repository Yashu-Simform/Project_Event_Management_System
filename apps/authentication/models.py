from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.core.validators import validate_email


# Create your models here.
class EmsUser(AbstractUser):
    email = models.EmailField(null=False, validators=[validate_email])
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="ems_user_set",
        related_query_name="ems_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="ems_user_set",
        related_query_name="ems_user",
    )