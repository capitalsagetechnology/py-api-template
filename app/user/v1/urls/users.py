from django.urls import include, path
from rest_framework.routers import DefaultRouter
from user.v1.views import UserVieSets, RedPandaDemoViewSet

app_name = "user"

router = DefaultRouter()
router.register('redpanda', RedPandaDemoViewSet, basename='redpanda')
router.register("", UserVieSets, basename='users')

urlpatterns = [
    path("", include(router.urls)),
]
