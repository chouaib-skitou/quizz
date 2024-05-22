from django.db import models

class Device(models.Model):
    ip_address = models.CharField(max_length=100)

    def __str__(self):
        return self.ip_address


class Controller(models.Model):
    TYPE_CHOICES = (
        ('sensor', 'Sensor'),
        ('button', 'Button'),
        ('other', 'Other'),
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default='other')
    request_infos = models.JSONField()
    api_route = models.CharField(max_length=200)

    def __str__(self):
        return self.name