import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_EMAIL_TOPIC = os.getenv("KAFKA_EMAIL_TOPIC", "send_emails")
