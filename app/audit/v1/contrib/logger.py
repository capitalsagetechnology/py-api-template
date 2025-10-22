from typing import Literal, TypedDict
from xmlrpc.client import DateTime

from audit.models import AuditLog, LoginHistory


class EventDataType(TypedDict):
    audit_type: str
    user_id: str
    user_name: str
    user_email: str
    action: str
    ip_address: str
    status: Literal["success", "failure"]


class DeviceInfoDataType(TypedDict):
    user_agent: str
    ip_address: str
    user_id: str
    user_email: str
    user_phone: str
    user_name: str
    user_role: str
    device_name: str
    device_version: str
    device_os: str
    login_time: DateTime
    lga: str | None
    state: str | None
    address: str | None
    longitude: float | None
    latitude: float | None
    city: str | None
    country: str | None


def log_event(event: EventDataType):
    AuditLog.objects.create(**event)
    return {"status": "Logged", "payload": event}


def log_login_history_event(payload: DeviceInfoDataType):
    LoginHistory.objects.create(**payload)
    return {"status": "Logged", "payload": payload}
