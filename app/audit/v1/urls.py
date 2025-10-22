from audit.v1.views import AuditLogViewSets
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "audit"

router = DefaultRouter()
router.register("", AuditLogViewSets, basename="audit")

urlpatterns = [
    path("", include(router.urls)),
]
