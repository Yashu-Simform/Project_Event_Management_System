from celery import shared_task
from .utils import send_invite_mail


@shared_task
def send_reminder_mail(context, recipient_list):
    subject = f"Reminder for event: {context['title']}"
    html_template = "EventReminderMailTemplate.html"
    send_invite_mail(subject, context, recipient_list, html_template)


@shared_task
def sub(x, y):
    return x - y
