from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

unit_srid = 4326


class Location(models.Model):
    url = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=200)
    point = models.PointField(srid=unit_srid, null=True, blank=True)
    lng = models.FloatField(verbose_name='Longitude')
    lat = models.FloatField(verbose_name='Latitude')

    objects = models.GeoManager()

    def save(self, *args, **kwargs):
        self.point = Point(self.lng, self.lat)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    phone_number = models.CharField(max_length=22, blank=True, null=True)
    location = models.ForeignKey(Location, related_name='profile', blank=True, null=True)

    def __str__(self):
        return str("{}".format(self.user))


class Event(models.Model):
    title = models.CharField(max_length=200)
    time = models.DateTimeField(default=datetime.now() + timedelta(days=1))
    location = models.ForeignKey(Location, related_name='events')
    users = models.ManyToManyField(UserProfile, related_name='events', blank=True)
    extras = models.TextField(blank=True)

    def __str__(self):
        return str(self.title)
