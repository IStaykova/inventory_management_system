from django.conf import settings
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
import logging

logger = logging.getLogger(__name__)


def send_template_email(*, to_email, template_id, dynamic_data):
    if not settings.SENDGRID_API_KEY or not settings.SENDGRID_FROM_EMAIL or not template_id:
        logger.warning("SendGrid is not configured properly.")
        return False

    try:
        message = Mail(
            from_email=settings.SENDGRID_FROM_EMAIL,
            to_emails=to_email,
        )
        message.template_id = template_id
        message.dynamic_template_data = dynamic_data

        client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = client.send(message)

        if response.status_code not in (200, 202):
            logger.error(
                "SendGrid failed. status=%s body=%s headers=%s",
                response.status_code,
                response.body,
                response.headers,
            )
            return False

        return True

    except Exception:
        logger.exception("Email sending failed.")
        return False