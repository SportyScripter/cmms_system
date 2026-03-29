from django.shortcuts import render
from rest_framework import viewsets
from .models import Machine, WorkOrder
from .serializers import MachineSerializer, WorkOrderSerializer


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer


class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
