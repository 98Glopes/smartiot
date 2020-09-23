from django.contrib.auth.models import User
from django.db import models

DATA_TYPE_CHOICES = (
    ('i', 'int'),
    ('f', 'float'),
    ('s', 'string')
)


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    area = models.CharField(max_length=30)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Sensor(models.Model):
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
    gateway_id = models.CharField(max_length=30)
    rssi = models.FloatField()
    snr = models.FloatField()
    value = models.CharField(max_length=30)
