from celery import shared_task
from core.utils import send_mail_ems
from core.utils import tomorrows_events


@shared_task
def send_reminder_mail(context, recipient_list):
    subject = f"Reminder for event: {context['title']}"
    html_template = "EventReminderMailTemplate.html"
    send_mail_ems(subject, context, recipient_list, html_template)


@shared_task
def sub(x, y):
    return x - y

@shared_task
def tomorrow_events_mail():
    mail_data = tomorrows_events()
    print(mail_data)
    send_mail_ems(**mail_data)