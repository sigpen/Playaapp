from django.contrib import admin

from footy import models

admin.site.register(models.UserProfile)
admin.site.register(models.Event)
admin.site.register(models.Location)

