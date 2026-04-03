from django.contrib import admin
from .models import Category, Part, InventoryLog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = (
        "unique_code",
        "name",
        "category",
        "get_machines",
        "quantity",
        "location",
        "is_low_stock_display",
    )
    list_filter = ("category", "location")
    search_fields = ("name", "unique_code", "type_model", "machines__name")
    filter_horizontal = ("machines",)

    @admin.display(boolean=True, description="Stan OK")
    def is_low_stock_display(self, obj):
        return not obj.is_low_stock()

    @admin.display(description="Pasuje do maszyny")
    def get_machines(self, obj):
        machines = obj.machines.all()[:3]
        names = [m.name for m in machines]
        if obj.machines.count() > 3:
            names.append("...")
        return ", ".join(names)


@admin.register(InventoryLog)
class InventoryLogAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp",
        "transaction_type",
        "part",
        "quantity",
        "user",
        "work_order",
    )
    list_filter = ("transaction_type", "timestamp", "user")
    search_fields = ("part__name", "part__unique_code", "work_order__title")

    def get_random_fields(self, obj):
        if obj:
            return (
                "part",
                "user",
                "work_order",
                "transaction_type",
                "quantity",
                "timestamp",
                "notes",
            )
        return "timestamp"
