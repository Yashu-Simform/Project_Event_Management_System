from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from api.models import Invite, Event
from apps.authentication.models import EmsUser
from .utils import send_mail_ems
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from .tasks import send_reminder_mail
from datetime import timedelta
from django.utils import timezone
from django.db import connection


@receiver(post_save, sender=Invite)
def send_invitation_mail(sender, instance: Invite, created, **kwargs):
    print("Signal called ")
    
    try:
        event = Event.objects.get(event_id=instance.event.event_id)
    except Event.DoesNotExist as e:
        raise e

    context = {
        "title": event.title,
        "description": event.description,
        "venue": event.venue,
        "event_time": event.event_time,
        "invite_id": instance.invite_id,
    }

    try:
        
        if instance.req_type == "Invitation":
            subject = f"Invitation for event: {event.title}"
            html_template="invitation_template.html"
        else:
            subject = f"Request to participate for event: {event.title}"
            html_template="participation_request_mail.html"

        send_mail_ems(
            subject,
            context,
            [instance.receiver_email],
            html_template=html_template,
        )

        # Schedule reminder mail
        if instance.req_type == "Invitation":
            eta_argu = context["event_time"] - timedelta(minutes=2)
            if eta_argu >= timezone.now():
                send_reminder_mail.apply_async(
                    (context, [instance.receiver_email]),
                    eta=eta_argu,
                    expires=context["event_time"],
                )
    except Exception as e:
        raise e

@receiver(pre_save, sender=Invite)
def invite_pre_save(sender, instance: Invite, **kwargs):
    # Checking whether the instance is already created. 
    if instance.invite_id:
        event_id = instance.event.event_id
        with connection.cursor() as cursor:
            # cursor.execute(sql="CALL update_total_participants(%s)", params=[event_id])
            cursor.execute(sql="CALL update_total_participants_v2(%s, %s);", params=[instance.invite_id, instance.status])
        return