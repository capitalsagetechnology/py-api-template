#!/bin/sh

python manage.py migrate --no-input
#python manage.py seed_wallet
#python manage.py seed_settings
#python manage.py seed_transfer_provider
#python manage.py seed_charge_fees
#python manage.py seed_vas_providers

exec "$@"
