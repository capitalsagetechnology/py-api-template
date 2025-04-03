import logging

from core.tasks import send_log_to_opensearch
from django.utils import timezone


class OpenSearchLogHandler(logging.Handler):
    def emit(self, record):
        try:
            # Convert log message to JSON if it's already structured, else keep it as a string
            if isinstance(record.msg, dict):
                message = record.msg  # Keep structured logs as-is
            else:
                message = str(
                    record.msg
                )  # Ensure it's a string if not already structured

            log_data = {
                "timestamp": timezone.now().isoformat(),  # Ensure proper timestamp format
                "level": record.levelname,
                "message": message,  # OpenSearch now gets a proper string/object
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
                "source": "django-log",
            }
            send_log_to_opensearch.apply_async(
                args=["django-logs", log_data], queue="logging_queue"
            )  # Send to logging queue
        except Exception as e:
            print(f"Logging Error: {e}")
