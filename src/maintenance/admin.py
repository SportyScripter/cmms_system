from django.contrib import admin
from .models import Machine, WorkOrder


# Register your models here.
@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("name", "serial_number", "location", "status")
    list_filer = ("status", "location")
    search_fields = ("name", "serial_number", "manufacturer")


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ("title", "machine", "priority", "status", "created_at")
    list_filter = ("status", "priority", "created_at")
    search_fields = ("title", "description", "machine__name", "machine__serial_number")
    date_hierarchy = "created_at"
