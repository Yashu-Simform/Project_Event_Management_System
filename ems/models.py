from django.db import models

# Create your models here.
class Event(models.Model):
    event_id = models.IntegerField(verbose_name='event_id', primary_key=True, auto_created=True, blank=True, null=False)
    host = models.ForeignKey('User.id')
    create_timestamp = models.DateTimeField(auto_now=True, auto_created=True, null=True, blank=True)
    event_time = models.DateTimeField(auto_now=False, auto_created=False, blank=False, null=False)
    venue = models.TextField(blank=False, null=False)
    total_participants = models.IntegerField(default=0, db_default=0)