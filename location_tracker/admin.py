from django.contrib import admin

from location_tracker.models import UserLocation, GeoLocation

admin.site.register(GeoLocation)
admin.site.register(UserLocation)
