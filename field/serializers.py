from datetime import  timedelta
from django.utils import timezone

from rest_framework import serializers
from .models import FootballField, FieldImage, Reservation, Review
from users.serializers import UserDetailSerializer

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','field', 'user', 'rating', 'comment', 'created_at']

class FieldImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldImage
        fields = ['id', 'image']


class FootballFieldSerializer(serializers.ModelSerializer):
    images = FieldImageSerializer(many=True, read_only=True)
    owner = UserDetailSerializer(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    distance = serializers.FloatField(read_only=True)
    geo_field = 'location'

    class Meta:
        model = FootballField
        fields = ['id', 'name', 'address', 'contact', 'price_per_hour', 'owner', 'images','location', 'average_rating', 'reviews', 'distance']

class ReservationSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'field', 'user', 'start_time', 'end_time','total_price']

    def validate(self, data):
        data = super().validate(data)

        if data['end_time'] - data['start_time'] < timedelta(hours=1):
            raise serializers.ValidationError("Minimum booking duration is 1 hour")

        if data['start_time'] < timezone.now():
            raise serializers.ValidationError("Cannot make reservations in the past")

        overlapping = Reservation.objects.filter(
            field=data['field'],
            start_time__lt=data['end_time'],
            end_time__gt=data['start_time']
        ).exists()
        if overlapping:
            raise serializers.ValidationError("This time slot is already booked")

        return data