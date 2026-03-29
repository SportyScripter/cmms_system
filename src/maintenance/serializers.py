from rest_framework import serializers
from .models import Machine, WorkOrder


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
            "mechine_name",
            "title",
            "description",
            "priority",
            "status",
            "photo",
            "created_at",
            "updated_at",
            "completion_at",
        ]
