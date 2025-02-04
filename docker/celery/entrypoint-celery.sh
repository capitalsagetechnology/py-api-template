#!/bin/sh

celery -A core worker --loglevel=info --concurrency=2 --hostname=worker1@%h --detach
celery -A core worker --loglevel=info --concurrency=2 --hostname=worker2@%h --detach
celery -A core worker --loglevel=info --concurrency=2 --hostname=worker3@%h --detach
celery -A core worker --loglevel=info --concurrency=2 --hostname=worker4@%h --detach

celery -A core beat -l debug --detach
exec "$@"


