from django.contrib import admin

from .models import Vehicle, TimeSlot

admin.site.register(Vehicle)

class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'start', 'end', 'user',)
    list_filter = ['start']

admin.site.register(TimeSlot, TimeSlotAdmin)
