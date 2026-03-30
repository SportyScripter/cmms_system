from rest_framework import viewsets
from .models import Part, InventoryLog
from .serializers import PartSerializer, InventoryLogSerializer


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class InventoryLogViewSet(viewsets.ModelViewSet):
    queryset = InventoryLog.objects.select_related('part', 'user', 'work_order')
    serializer_class = InventoryLogSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
