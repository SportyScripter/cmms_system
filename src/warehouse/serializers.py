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

    def validate(self, attrs):
        """
        Enforce business rules for inventory transactions:
        - quantity must be strictly greater than zero
        - ISSUE transactions cannot request more than available stock
        """
        part = attrs.get("part") or getattr(self.instance, "part", None)
        quantity = attrs.get("quantity", getattr(self.instance, "quantity", None))
        transaction_type = attrs.get(
            "transaction_type", getattr(self.instance, "transaction_type", None)
        )

        if quantity is None or quantity <= 0:
            raise serializers.ValidationError(
                {"quantity": "Quantity must be greater than zero."}
            )

        _ttype = str(transaction_type).upper() if transaction_type is not None else ""
        if _ttype == "ISSUE":
            if part is None:
                raise serializers.ValidationError(
                    {"part": "Part must be specified for ISSUE transactions."}
                )
            if quantity > part.quantity:
                raise serializers.ValidationError(
                    {"quantity": "Requested quantity exceeds available stock."}
                )

        return attrs
