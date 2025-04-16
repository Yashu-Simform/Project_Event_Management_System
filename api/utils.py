from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from ems.emsmodels import *


def send_invite_mail(
    subject, context, recipient_list, html_template="invitation_template.html"
):
    from_email = settings.EMAIL_HOST_USER
    # send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)

    html_content = render_to_string(html_template, context={"e": context})
    msg = EmailMultiAlternatives(subject, html_content, from_email, recipient_list)
    msg.content_subtype = "html"
    msg.send()
