from django.dispatch import receiver
from django.db.models.signals import post_save
from ems.emsmodels import *
from .utils import send_invite_mail

@receiver(post_save, sender = Invite)
def send_invitation_mail(sender, **kwargs):
    print(sender, kwargs)
    # try:
    #     event = Event.objects.get(event_id=instance.event)
    # except Event.DoesNotExist as e:
    #     raise e
    
    # context = {
    #     'title': event.title,
    #     'description': event.description,
    #     'venue': event.venue,
    #     'event_time': event.event_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    #     'invite_id': instance.invite_id,
    # }
    # try:
    #     send_invite_mail(f"Invitation for event: {event.title}", context, [instance.invite_to])
    # except Exception as e:
    #     raise e