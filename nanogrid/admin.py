from django.contrib import admin

from .models import Vehicle, TimeSlot, Issue

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'type', 'serial_number', 'battery', 'created_date')

admin.site.register(Vehicle, VehicleAdmin)

class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'start', 'end', 'user',)
    list_filter = ['start']

admin.site.register(TimeSlot, TimeSlotAdmin)

class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vehicle', 'comment', 'created_date',)
    list_filter = ['created_date']

admin.site.register(Issue, IssueAdmin)
