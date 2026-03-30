from rest_framework import viewsets
from .models import Part , InventoryLog
from .serializers import PartSerializer, InventoryLogSerializer


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class InventoryLogViewSet(viewsets.ModelViewSet):
    queryset = InventoryLog.objects.all()
    serializer_class = InventoryLogSerializer
