from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from warehouse.views import PartViewSet, InventoryLogViewSet
from maintenance.views import (
    MachineViewSet,
    WorkOrderViewSet,
    MaintenanceScheduleViewSet,
)
from accounts.views import UserViewSet

router = DefaultRouter()
router.register(r"parts", PartViewSet)
router.register(r"inventory-logs", InventoryLogViewSet)
router.register(r"machines", MachineViewSet)
router.register(r"work-orders", WorkOrderViewSet)
router.register(r"users", UserViewSet)
router.register(r"schedules", MaintenanceScheduleViewSet)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
