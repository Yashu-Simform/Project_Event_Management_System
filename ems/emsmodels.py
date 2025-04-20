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



class Event(models.Model):
    event_id = models.AutoField(
        verbose_name="event_id",
        primary_key=True,
        auto_created=True,
        blank=True,
        null=False,
    )  # PK
    host = models.ForeignKey(to=EmsUser, on_delete=models.CASCADE)  # FK -> User
    create_timestamp = models.DateTimeField(
        auto_now=True, auto_created=True, null=True, blank=True
    )
    event_time = models.DateTimeField(
        auto_now=False, auto_created=False, blank=False, null=False
    )
    venue = models.TextField(blank=False, null=False)
    total_participants = models.IntegerField(default=0, db_default=0)
    title = models.CharField(max_length=255, null=False, default="An event")
    description = models.TextField(db_default="")
    event_type = models.CharField(
        verbose_name="event_type",
        choices={"private": "Private", "public": "Public"},
        default="Private",
        db_default="private",
        max_length=15,
    )

    def clean(self):
        if self.total_participants < 0:
            raise Exception('Number of participants can not be negative.')
        return super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Invite(models.Model):
    invite_id = models.AutoField(
        verbose_name="invite_id",
        primary_key=True,
        auto_created=True,
        blank=True,
        null=False,
    )  # PK
    invite_from = models.ForeignKey(
        verbose_name="from",
        to=EmsUser,
        on_delete=models.CASCADE,
        related_name="invite_from",
        blank=True,
        null=False,
    )  # FK -> User
    invite_to = models.ForeignKey(
        verbose_name="to",
        to=EmsUser,
        on_delete=models.CASCADE,
        null=False,
        related_name="invite_to",
        blank=True,
    )  # FK -> User
    receiver_email = models.EmailField(
        verbose_name="receiver_email",
        blank=False,
        null=False,
        default="anonymususer@ems.com",
    )
    status = models.CharField(
        verbose_name="status",
        choices={"pending": "Pending", "accepted": "Accepted", "declined": "Declined"},
        default="Pending",
        db_default="pending",
    )
    create_timestamp = models.DateTimeField(
        auto_now=True, auto_created=True, null=True, blank=True
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, blank=True, null=False, related_name='event_invites'
    )  # FK -> Event
    req_type = models.CharField(
        choices={'invitation': 'Invitation', 'participation': 'Participation'},
        default='invitation',
        blank=True,
        null=False,
    )