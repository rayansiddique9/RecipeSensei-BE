"""This module contains the celery task to send verification link to the email provided when user registers.
"""
import logging
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


logger = logging.getLogger("scheduler")

@shared_task(name="tasks.send_verification_email")
def send_verification_email(recepient_email, verification_url):
    """This method uses the verfication email template and sends the email to the recepient.

    Args:
        email (string): Recepient email.
        verification_url (string): The url path for the verify-email view.
    """
    subject = "Email Verification"
    html_message = render_to_string(
        "verification_email.html",
        {
            "verification_url": verification_url
        }
    )
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [recepient_email,]
    
    try:
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message, fail_silently=False)
        logger.info("Verification email sent.")
        logger.info(verification_url)

    except Exception as error:
        logger.error(f"Error in sending verification email.\n{error}")

