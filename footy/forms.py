from django import forms
from django.contrib.auth.models import User

from footy.models import UserProfile, Event


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


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'title',
            'time',
            'location',
            'users',
            'extras',
        )
