from audit.models import AuditLog
from audit.v1.serializers import AuditLogSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny


class AuditLogViewSets(viewsets.ModelViewSet):
    """Agent viewsets"""

    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get", "post"]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["audit_type", "user_email", "ip_address", "created_at"]
    search_fields = ["user_name", "user_email", "action", "ip_address", "audit_type"]
    ordering_fields = ["created_at"]
