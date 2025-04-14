from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

def send_invite_mail(subject, context, recipient_list):
    from_email = settings.EMAIL_HOST_USER
    # send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)

    ctx = context.copy()
    event_time = ctx.pop('event_time')
    event_time = event_time.replace('T', ' ').replace('Z', '')
    event_date_time = event_time.split(' ')
    ctx['event_date'] = event_date_time[0]
    ctx['event_time'] = event_date_time[1]
    html_content = render_to_string('invitation_template.html', context={'e': ctx})
    msg = EmailMultiAlternatives(subject, html_content, from_email, recipient_list)
    msg.content_subtype = 'html'
    msg.send()