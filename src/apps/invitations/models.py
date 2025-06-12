from django.db import models
from src.apps.authentication.models import EmsUser
from src.apps.events.models import Event

# Create your models here.
class Invite(models.Model):
    invite_id = models.AutoField(
        verbose_name="invite_id",
        primary_key=True,
        auto_created=True,
        blank=True,
        null=False,
    )  # PK
    sent_from = models.ForeignKey(
        verbose_name="from",
        to=EmsUser,
        on_delete=models.CASCADE,
        related_name="sent_from",
        blank=True,
        null=False,
    )  # FK -> User
    sent_to = models.ForeignKey(
        verbose_name="to",
        to=EmsUser,
        on_delete=models.CASCADE,
        null=False,
        related_name="sent_to",
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