# notifications/services.py
from .kafka_producer import send_email_event

def send_welcome_email_async(user: dict):
    subject = "Welcome!"
    body = f"Hi {user['firstname']}, welcome on board."
    html_body = f"<p>Hi <strong>{user['firstname']}</strong>, welcome on board.</p>"
    send_email_event(user['email'], subject, body, html_body)
