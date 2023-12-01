from django.contrib import admin

# Register your models here.

from .models import Device, Variable, DeviceData, Alarm

admin.site.register(Device)
admin.site.register(Variable)

admin.site.register(DeviceData)
admin.site.register(Alarm)