from django.contrib import admin
from apps.api.models import Device, Sensor, Read

admin.site.register(Device)
admin.site.register(Sensor)
admin.site.register(Read)

