from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    event_id = models.IntegerField(verbose_name='event_id', primary_key=True, auto_created=True, blank=True, null=False)    #PK
    host = models.ForeignKey(to=User, on_delete=models.CASCADE)    #FK -> User
    create_timestamp = models.DateTimeField(auto_now=True, auto_created=True, null=True, blank=True)
    event_time = models.DateTimeField(auto_now=False, auto_created=False, blank=False, null=False)
    venue = models.TextField(blank=False, null=False)
    total_participants = models.IntegerField(default=0, db_default=0)

class Invite(models.Model):
    invite_id = models.IntegerField(verbose_name='invite_id', primary_key=True, auto_created=True, blank=True, null=False)  #PK
    invite_from = models.ForeignKey(verbose_name='from', to=User, on_delete=models.CASCADE, related_name='invite_from') #FK -> User
    invite_to = models.ForeignKey(verbose_name='to', to=User, on_delete=models.CASCADE, null = True, related_name='invite_to')    #FK -> User
    status = models.CharField(verbose_name='status', choices={'pending' : 'Pending', 'accepted' : 'Accepted', 'rejected': 'Rejected'})
    create_timestamp = models.DateTimeField(auto_now=True, auto_created=True, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  #FK -> Event