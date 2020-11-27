from django.contrib.auth.models import User
from django.db import models

from apps.api.utils import get_random_string

DATA_TYPE_CHOICES = (
    ('i', 'int'),
    ('f', 'float'),
    ('s', 'string')
)
DATA_TYPE_CAST = {
    'i': int,
    'f': float,
    's': str,
}


class Device(models.Model):
    id = models.CharField(max_length=4, primary_key=True, default=get_random_string)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    area = models.CharField(max_length=30)

    mqtt_user = models.CharField(max_length=6)
    mqtt_passwd = models.CharField(max_length=6)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Sensor(models.Model):
    id = models.CharField(max_length=4, primary_key=True, default=get_random_string)
    name = models.CharField(max_length=30)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    data_type = models.CharField(max_length=7, choices=DATA_TYPE_CHOICES, blank=False, null=False)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Read(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(editable=True, null=False, blank=False)
    raw_value = models.CharField(max_length=30)

    @property
    def value(self):
        cast = DATA_TYPE_CAST[self.sensor.data_type]
        return cast(self.raw_value)

    def __str__(self):
        return F"{self.sensor.device.id}.{self.sensor.id}.{self.timestamp}"
