import uuid

from django.db import models


class AuditLog(models.Model):
    objects = models.Manager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    audit_type = models.CharField(max_length=255, db_index=True)
    user_id = models.CharField(max_length=255, db_index=True)
    user_name = models.CharField(max_length=255, db_index=True)
    user_email = models.EmailField(db_index=True)
    action = models.TextField()
    ip_address = models.GenericIPAddressField()
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    log_data = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user_name} - {self.action}"


class LoginHistory(models.Model):
    objects = models.Manager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=255, db_index=True)
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField(db_index=True, null=True)
    user_phone = models.CharField(max_length=255, null=True)
    user_role = models.CharField(max_length=255, null=True)
    device_name = models.CharField(max_length=255, null=True, blank=True)
    device_version = models.CharField(max_length=255, null=True, blank=True)
    device_os = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.TextField(null=True)
    login_time = models.DateTimeField(null=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    lga = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.user_id
