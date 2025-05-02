from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from ems.emsmodels import *
from datetime import timedelta, datetime
from django.utils import timezone


def send_mail_ems(
    subject, context, recipient_list, html_template="invitation_template.html", context_obj_name = 'e'
):
    from_email = settings.EMAIL_HOST_USER
    # send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)

    html_content = render_to_string(html_template, context={context_obj_name: context})
    msg = EmailMultiAlternatives(subject, html_content, from_email, recipient_list)
    msg.content_subtype = "html"
    msg.send()

def tomorrows_events():
    from ems.emsmodels import Event

    tomorrow = timezone.now() + timezone.timedelta(days=1)
    tomorrow_start = tomorrow.replace(hour=0,minute=0,second=0,microsecond=0)
    tomorrow_end = tomorrow_start + timezone.timedelta(days=1)
    qs = Event.objects.filter(event_type="public", event_time__gte=tomorrow_start, event_time__lt=tomorrow_end).values('title', 'event_time')
    context = list(qs)

    subject = "Tomorrow's Events: "
    # html_content = render_to_string("Tomorrow_Event.html", context=context)
    recipient_list = list(EmsUser.objects.values_list('email', flat=True))

    return {
        'subject': subject,
        'context': context,
        'recipient_list': [recipient_list[1]], # For testing only
        # 'recipient_list': recipient_list,
        'html_template': "Tomorrow_Event.html",
        'context_obj_name': 'events'
    }