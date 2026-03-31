from django.shortcuts import render
from rest_framework import viewsets
from .models import Machine, WorkOrder, MaintenanceSchedule
from .serializers import (
    MachineSerializer,
    WorkOrderSerializer,
    MaintenanceScheduleSerializer,
)


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer


class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer


class MaintenanceScheduleViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceSchedule.objects.all()
    serializer_class = MaintenanceScheduleSerializer

    def get_queryset(self):
        queryset = MaintenanceSchedule.objects.all()
        month = self.request.query_params.get("month")
        year = self.request.query_params.get("year")
        if month and year:
            queryset = queryset.filter(
                next_due_date__month=month, next_due_date__year=year
            )
        return queryset
