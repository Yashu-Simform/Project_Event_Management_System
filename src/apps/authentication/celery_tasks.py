from celery import shared_task
from core.utils import send_mail_ems
from core import settings

@shared_task
def send_otp_email(
    *,
    subject="Verify OTP to get authenticated!",
    otp_as_context="",
    recipient_list=[],
    html_template="otp_email_template.html",
    context_obj_name="otp"
):
    if not otp_as_context:
        settings.logging.debug('Provided OTP is None!')
    send_mail_ems(subject, otp_as_context, recipient_list, html_template, context_obj_name)
