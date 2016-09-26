from django.contrib import admin
from django import forms

from footy import models
from footy.models import Location

# Add models to admin's website page
admin.site.register(models.UserProfile)
admin.site.register(models.Event)

