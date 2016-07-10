from rest_framework import serializers

from footy import models


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = (
            'url',
            'title',
        )


class UserProfileSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = models.UserProfile
        fields = (
            'user',
            'phone_number',
            'location',
        )


class EventSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    users = UserProfileSerializer(many=True)

    class Meta:
        model = models.Location
        fields = (
            'title',
            'time',
            'location',
            'users',
            'extras',
        )
