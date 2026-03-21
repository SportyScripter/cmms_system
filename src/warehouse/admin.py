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
        "assigment",
        "quantity",
        "location",
        "is_low_stock_display",
    )
    list_filter = ("category", "location")
    search_fields = ("name", "unique_code", "type_model", "assigment")

    @admin.display(boolean=True, description="Stan OK")
    def is_low_stock_display(self, obj):
        return not obj.is_low_stock()
