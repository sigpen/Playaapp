from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

unit_srid = 4326


# Creating database

# Location field
class Location(models.Model):
    url = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=200)
    point = models.PointField(srid=unit_srid, null=True, blank=True)
    lng = models.FloatField(verbose_name='Longitude')
    lat = models.FloatField(verbose_name='Latitude')

    objects = models.GeoManager()

    # Create a Google Maps url with Latitude & Longtitude as values.
    # Save Latitude & Longtitude (Float fields) as Point (PointField).
    def save(self, *args, **kwargs):
        self.url = "http://maps.google.com/?q={},{}".format(self.lat, self.lng)
        self.point = Point(self.lng, self.lat)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)


# UserProfile field.
# User field is a FK to Django's AUTH USER MODEL containing: username, password and email address.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    phone_number = models.CharField(max_length=22, blank=True, null=True)
    location = models.ForeignKey(Location, related_name='profile', blank=True, null=True)

    def __str__(self):
        return str("{}".format(self.user))


# Event field (Matches)
class Event(models.Model):
    title = models.CharField(max_length=200)
    time = models.DateTimeField(default=datetime.now() + timedelta(days=1))
    location = models.ForeignKey(Location, related_name='events')
    users = models.ManyToManyField(UserProfile, related_name='events', blank=True)
    extras = models.TextField(blank=True)

    def __str__(self):
        return str(self.title)
