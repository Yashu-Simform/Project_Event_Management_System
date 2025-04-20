from django.dispatch import receiver
from django.db.models.signals import post_save
from ems.emsmodels import *
from .utils import send_mail_ems
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from .tasks import send_reminder_mail
from datetime import timedelta
from django.utils import timezone
from django.db import connection


@receiver(post_save, sender=Invite)
def send_invitation_mail(sender, instance, created, **kwargs):
    print("Signal called ")
    if not created:
        # POST Update
        event_id = instance.event.event_id
        with connection.cursor() as cursor:
            cursor.execute(sql="CALL update_total_participants(%s)", params=[event_id])
        return
    
    
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

    print("Event time dirs: ", dir(event.event_time))
    try:
        send_mail_ems(
            f"Invitation for event: {event.title}",
            context,
            [instance.receiver_email],
            html_template="invitation_template.html",
        )

        # Schedule reminder mail
        eta_argu = context["event_time"] - timedelta(minutes=2)
        if eta_argu >= timezone.now():
            send_reminder_mail.apply_async(
                (context, [instance.receiver_email]),
                eta=eta_argu,
                expires=context["event_time"],
            )
    except Exception as e:
        raise e
