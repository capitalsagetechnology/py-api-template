#!/bin/sh

# celery -A core worker -c 4 --loglevel=info --logfile=logs/celery.log --detach
celery -A core worker -c 4 --loglevel=info --detach
celery -A core beat -l debug --detach
#celery --broker=${REDIS_URL} flower --port=5555
exec "$@"
