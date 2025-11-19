import json
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand

from confluent_kafka import Consumer, KafkaError

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Consume email events from Redpanda/Kafka and send emails"

    def handle(self, *args, **options):
        consumer = Consumer({
            "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
            "group.id": "email_sender_group",
            "auto.offset.reset": "earliest",  # 'latest' in prod if you prefer
            "enable.auto.commit": True,
        })

        topic = settings.KAFKA_EMAIL_TOPIC
        consumer.subscribe([topic])

        self.stdout.write(self.style.SUCCESS(f"Listening on topic '{topic}'"))

        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() != KafkaError._PARTITION_EOF:
                        logger.error("Kafka error: %s", msg.error())
                    continue

                try:
                    payload = json.loads(msg.value().decode("utf-8"))
                    self._process_email_payload(payload)
                except Exception:
                    logger.exception("Failed to process message")
        except KeyboardInterrupt:
            self.stdout.write("Stopping consumer...")
        finally:
            consumer.close()

    def _process_email_payload(self, payload: dict):
        to_email = payload.get("to_email")
        subject = payload.get("subject")
        body = payload.get("body", "")
        html_body = payload.get("html_body")

        if not to_email or not subject:
            logger.warning("Invalid payload: %s", payload)
            return

        msg = EmailMultiAlternatives(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        if html_body:
            msg.attach_alternative(html_body, "text/html")

        msg.send()
        logger.info("Sent email to %s", to_email)
