from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from src.apps.authentication.models import EmsUser
from src.apps.events.models import Event
from src.apps.invitations.models import Invite
from django.utils import timezone
from string import punctuation
from rest_framework.response import Response
from rest_framework import status

def success_response(*,status=status.HTTP_200_OK, message = '', data = {}):
    return Response(
        {
            'success': True,
            'message': message,
            'data': data
        },
        status=status
    )

def error_response(*, status=status.HTTP_500_INTERNAL_SERVER_ERROR, message='', error={}):
    return Response(
        {
            'success': False,
            'message': message,
            'error': error
        },
        status=status
    )

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

def check_password_complexity(value: str):
    if len(value) < 8:
        raise ValueError('Invalid Password! Password must contains at least 8 characters.')
    
    if len(value) > 64:
        raise ValueError('Invalid Password! Password must contains at max 64 characters.')
    
    has_lowercase = False
    has_uppercase = False
    has_digit = False
    has_special_char = False

    for c in value:
        if c.isalpha():
            if c.islower():
                has_lowercase = True
            if c.isupper():
                has_uppercase = True

        if c.isdigit():
            has_digit = True

        if c in punctuation:
            has_special_char = True

    if not (has_lowercase and has_uppercase and has_digit and has_special_char):
        raise ValueError('Invalid Password! Password must contain at least 1 lowercase, 1 uppercase, 1 digit and 1 special character.')
    
    return value