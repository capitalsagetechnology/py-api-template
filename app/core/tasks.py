import datetime

from celery.app import shared_task
from core import settings
from opensearchpy import OpenSearch

host = "143.110.171.18"
port = 9200
auth = ("admin", "Fxw6GlbaXu0sJWUG")
# ca_certs_path = '/full/path/to/root-ca.pem'
# Provide a CA bundle if you use intermediate CAs with your root CA.

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts=["https://143.110.171.18:9200"],
    http_auth=auth,
    http_compress=True,  # enables gzip compression for request bodies
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)


@shared_task(queue="logging_queue")
def send_log_to_opensearch(source, message):
    index_name = f"wallet-api-{settings.ENVIRONMENT_INSTANCE}"
    log_entry = {
        "timestamp": str(datetime.datetime.now()),
        "level": "info",
        "message": message,
        "source": index_name,
        "settings.ENVIRONMENT_INSTANCE": settings.ENVIRONMENT_INSTANCE,
    }

    client.index(index=index_name, body=log_entry)
    return log_entry
