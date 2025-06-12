from django.db import models
from src.apps.authentication.models import EmsUser

# Create your models here.
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
    total_participants = models.IntegerField(default=0, db_default=0) #Can be removed
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