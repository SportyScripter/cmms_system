from django.contrib import admin
from .models import Category, Part

# Register your models here.


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
