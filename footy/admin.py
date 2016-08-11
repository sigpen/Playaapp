from django.contrib import admin
from django import forms
from easy_maps.widgets import AddressWithMapWidget

from footy import models
from footy.models import Location

# Add models to admin's website page
admin.site.register(models.UserProfile)
admin.site.register(models.Event)


# Add location widget to admin's website page
class LocationAdmin(admin.ModelAdmin):
    class form(forms.ModelForm):
        class Meta:
            widgets = {
                'address': AddressWithMapWidget({'class': 'vTextField'})
            }


admin.site.register(Location, LocationAdmin)
