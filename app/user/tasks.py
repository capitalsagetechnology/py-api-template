from django.template.loader import get_template

from core.celery import APP
from .utils import send_email


@APP.task()
def send_registration_email(email_data):
    html_template = get_template('emails/account_verification_template.html')
    text_template = get_template('emails/account_verification_template.txt')
    html_alternative = html_template.render(email_data)
    text_alternative = text_template.render(email_data)
    send_email('Account Verification',
               email_data['email'], html_alternative, text_alternative)


@APP.task()
def send_password_reset_email(email_data):
    html_template = get_template('emails/password_reset_template.html')
    text_template = get_template('emails/password_reset_template.txt')
    html_alternative = html_template.render(email_data)
    text_alternative = text_template.render(email_data)
    send_email('Password Reset',
               email_data['email'], html_alternative, text_alternative)
