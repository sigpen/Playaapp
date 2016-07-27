from django import forms
from django.contrib.auth.models import User
from django.contrib.gis import forms as geoforms
from django.contrib.gis.geos import Point
from django.forms.models import inlineformset_factory

from footy.models import Event, Location

unit_srid = 4326


class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())
    phone_number = forms.CharField(max_length=200)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
        )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=300)
    password = forms.CharField(max_length=300, widget=forms.PasswordInput())


# class LocationForm(geomodels.Model):
#     url = geomodels.URLField()
#     title = geomodels.CharField(max_length=200)
#     points = geomodels.PointField(srid=unit_srid, null=True, blank=True)
#
#     class Meta:
#         model = Location
#         fields = (
#             'title',
#             'points',
#             'url',
#         )
#
#




EventFormSet = inlineformset_factory(Location, Event, fk_name='location', exclude=('point',))


class EventForm(forms.ModelForm):
    location_title = forms.CharField(max_length=300)

    # def save(self, commit=True):
    #     lng = self.cleaned_data['location_lng']
    #     lat = self.cleaned_data['location_lat']
    #     point = Point(lng, lat)
    #     title = self.cleaned_data['location_title']
    #     location = Location.objects.get_or_create(lng=lng, lat=lat, point=point, title=title)
    #     self.instance.location = location
    #
    #     return super().save(commit)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    # self.fields['lng'] = forms.FloatField(max_value=90)
    # self.fields['lat'] = forms.FloatField(max_value=90)

    class Meta:
        model = Event
        # exclude = (
        #     'location',
        # )

        fields = (
            'title',
            'time',
            # 'location_lng',
            # 'location_lat',
            'location',
            'users',
            'extras',
        )


class AddUserEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'users',
        )
