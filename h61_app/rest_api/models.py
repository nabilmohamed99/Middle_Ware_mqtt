# myapp/models.py
from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=100)

class Variable(models.Model):

    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    description = models.TextField()

class DeviceData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True,db_index=True)
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE,null=True,db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    value = models.FloatField()

class Alarm(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    message = models.TextField()

class Command(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    command = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
