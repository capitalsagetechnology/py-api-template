from audit.models import LoginHistory
from common.admin import ReadOnlyModelAdmin
from django.contrib import admin


@admin.register(LoginHistory)
class LoginHistoryAdmin(ReadOnlyModelAdmin):
    list_display = (
        "user_id",
        "user_name",
        "user_email",
        "user_phone",
        "user_role",
        "ip_address",
        "longitude",
        "latitude",
        "country",
        "state",
        "lga",
        "city",
        "address",
        "user_agent",
        "login_time",
    )
    search_fields = ("user_email",)
