from django.conf import settings
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient


def send_template_email(*, to_email, template_id, dynamic_data):
    message = Mail(
        from_email=settings.SENDGRID_FROM_EMAIL,
        to_emails=to_email,
    )

    message.template_id = template_id
    message.dynamic_template_data = dynamic_data

    client = SendGridAPIClient(settings.SENDGRID_API_KEY)
    client.send(message)