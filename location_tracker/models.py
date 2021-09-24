from django.db import models
from django.utils import timezone


class GeoLocation(models.Model):
    location_id = models.IntegerField(primary_key=True)
    country_name = models.CharField(max_length=25)
    location_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.country_name} - {self.location_name}"


class UserLocation(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    location = models.ForeignKey(GeoLocation, on_delete=models.CASCADE)
    added_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.email}-{self.location}-{self.added_time}"
