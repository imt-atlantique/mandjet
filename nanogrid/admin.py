from django.contrib import admin

from .models import Vehicle, TimeSlot

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'type', 'serial_number', 'battery', 'created_date')

admin.site.register(Vehicle, VehicleAdmin)

class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'start', 'end', 'user',)
    list_filter = ['start']

admin.site.register(TimeSlot, TimeSlotAdmin)
