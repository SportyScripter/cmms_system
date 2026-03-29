from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

# --- JWT Authentication Endpoints ---
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from warehouse.views import PartViewSet
from maintenance.views import MachineViewSet, WorkOrderViewSet

router = DefaultRouter()
router.register(r"parts", PartViewSet)
router.register(r"machines", MachineViewSet)
router.register(r"work-orders", WorkOrderViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
