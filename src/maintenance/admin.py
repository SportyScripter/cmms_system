from django.contrib import admin
from .models import Machine, WorkOrder
from .models import MaintenanceSchedule


# Register your models here.
@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("name", "serial_number", "location", "status")
    list_filter = ("status", "location")
    search_fields = ("name", "serial_number", "manufacturer")


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ("title", "machine", "priority", "status", "created_at")
    list_filter = ("status", "priority", "created_at")
    search_fields = ("title", "description", "machine__name", "machine__serial_number")
    date_hierarchy = "created_at"


@admin.register(MaintenanceSchedule)
class MaintenanceScheduleAdmin(admin.ModelAdmin):
    list_display = ("title", "machine", "interval_days", "next_due_date", "is_active")
    list_filter = ("is_active", "next_due_date")
