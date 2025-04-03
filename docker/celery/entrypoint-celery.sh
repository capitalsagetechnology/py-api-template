#!/bin/sh

celery -A core worker --loglevel=info --concurrency=2 --hostname=worker1@%h --detach
celery -A core worker --loglevel=info --concurrency=2 --hostname=worker2@%h --detach
#celery -A core worker --loglevel=info --concurrency=2 --hostname=worker3@%h --detach

celery -A core worker --loglevel=info --queues=reversal_queue --concurrency=1 --hostname=reversal_worker@%h --prefetch-multiplier=1 --detach

celery -A core beat -l INFO --detach
celery -A core beat -l INFO --detach --scheduler django_celery_beat.schedulers:DatabaseScheduler

exec "$@"
