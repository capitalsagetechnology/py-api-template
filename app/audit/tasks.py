import logging

from audit.v1.contrib.logger import log_event, log_login_history_event
from core.celery import APP
from django.utils.timezone import now

logger = logging.getLogger(__name__)


@APP.task()
def log_audit_event_task(payload):
    return log_event(payload)


@APP.task()
def log_login_history_task(payload):
    return log_login_history_event(payload)


@APP.task()
def create_login_history_with_location_task(
    client_ip, user_agent, user_id, device_data
):
    from user.models import User
    from user.services.location import get_state_and_lga
    from user.tasks import register_location_task

    res = dict()
    try:
        res = get_state_and_lga(device_data["latitude"], device_data["longitude"])
        logger.info(res)
    except Exception as e:
        logger.info(f"Error decoding location: {e}")

    user = User.objects.get(id=user_id)
    login_history_payload = {
        "user_agent": user_agent,
        "ip_address": client_ip,
        "user_id": user.id,
        "user_email": user.email,
        "user_phone": user.phone,
        "user_name": user.fullname,
        "user_role": user.role,
        "device_name": device_data.get("device_name"),
        "device_version": device_data.get("device_version"),
        "device_os": device_data.get("device_os"),
        "login_time": now(),
        "lga": res.get("lga") if res else None,
        "state": res.get("state") if res else None,
        "address": res.get("address") if res else device_data.get("address"),
        "longitude": device_data.get("longitude", 0),
        "latitude": device_data.get("latitude", 0),
    }

    audit_payload = {
        "audit_type": "login_attempt",
        "user_id": user.id,
        "user_name": f"{user.fullname}",
        "user_email": user.email,
        "action": "User logs in",
        "ip_address": client_ip,
        "status": "success",
    }

    location_payload = {
        "agent_id": user.id,
        "name": f"{user.lastname} {user.firstname}",
        "email": user.email,
        "phone": user.phone if user.phone else user.email,
        "longitude": device_data.get("longitude", 0),
        "latitude": device_data.get("longitude", 0),
        "address": res.get("address") if res else device_data.get("address"),
    }

    log_audit_event_task.delay(audit_payload)
    log_login_history_task.delay(login_history_payload)
    register_location_task.delay(location_payload)

    return login_history_payload
