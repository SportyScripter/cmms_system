from rest_framework import serializers
from .models import Machine, WorkOrder, MaintenanceSchedule


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = "__all__"


class WorkOrderSerializer(serializers.ModelSerializer):
    machine_name = serializers.CharField(source="machine.name", read_only=True)

    class Meta:
        model = WorkOrder
        fields = [
            "id",
            "machine",
            "machine_name",
            "title",
            "description",
            "priority",
            "status",
            "photo",
            "created_at",
            "updated_at",
            "completed_at",
        ]


class MaintenanceScheduleSerializer(serializers.ModelSerializer):
    machine_name = serializers.CharField(source="machine.name", read_only=True)

    class Meta:
        model = MaintenanceSchedule
        fields = [
            "id",
            "title",
            "machine",
            "machine_name",
            "description",
            "interval_days",
            "next_due_date",
            "is_active",
        ]
