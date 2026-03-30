from rest_framework import serializers
from .models import Part, InventoryLog


class PartSerializer(serializers.ModelSerializer):
    machine_list = serializers.SerializerMethodField()

    class Meta:
        model = Part
        fields = [
            "id",
            "name",
            "unique_code",
            "quantity",
            "min_quantity",
            "location",
            "price",
            "machine_list",
            "barecode_image",
        ]

    def get_machine_list(self, obj):
        return [machine.name for machine in obj.machines.all()]


class InventoryLogSerializer(serializers.ModelSerializer):
    part_name = serializers.CharField(source="part.name", read_only=True)
    user_name = serializers.CharField(source="user.username", read_only=True)
    work_order_title = serializers.CharField(source="work_order.title", read_only=True)

    class Meta:
        model = InventoryLog
        fields = [
            "id",
            "part",
            "part_name",
            "user",
            "user_name",
            "work_order",
            "work_order_title",
            "transaction_type",
            "quantity",
            "timestamp",
            "notes",
        ]
        read_only_fields = ["timestamp"]
