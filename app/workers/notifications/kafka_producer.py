# notifications/kafka_producer.py
import json
from django.conf import settings
from confluent_kafka import Producer

producer = Producer({
    "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
})

def _delivery_report(err, msg):
    if err is not None:
        # swap this with logging/Sentry in your stack
        print(f"Delivery failed for record {msg.key()}: {err}")
    else:
        print(
            f"Record produced to {msg.topic()} [{msg.partition()}] offset {msg.offset()}"
        )

def send_email_event(
    to_email: str,
    subject: str,
    body: str,
    html_body: str | None = None,
):
    payload = {
        "to_email": to_email,
        "subject": subject,
        "body": body,
        "html_body": html_body,
    }

    producer.produce(
        topic=settings.KAFKA_EMAIL_TOPIC,
        value=json.dumps(payload).encode("utf-8"),
        callback=_delivery_report,
    )

    # for high-throughput you can skip this and flush periodically
    producer.flush()
