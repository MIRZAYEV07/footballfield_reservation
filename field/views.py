from django.db.models import Avg, Sum, F, ExpressionWrapper, fields, Count
from django.db.models.functions import Coalesce
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from users.models import User
from .models import FootballField, Reservation, Review
from .serializers import FootballFieldSerializer, ReservationSerializer, ReviewSerializer
from common.permissions import UpdateDeletePermission, CreatePermission, DeletePersonalObjectPermission, PersonalObjectPermission, UpdatePermission
from .filters import AvailableFieldFilter


class FootballFieldListCreateView(generics.ListCreateAPIView):
    serializer_class = FootballFieldSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CreatePermission]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AvailableFieldFilter
    ordering_fields = ['price_per_hour', 'average_rating', 'distance']

    def get_queryset(self):
        queryset = FootballField.objects.annotate(
            average_rating=Coalesce(Avg('reviews__rating'), 0.0)
        )

        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        if latitude and longitude:
            point = Point(float(longitude), float(latitude), srid=4326)
            queryset = queryset.annotate(distance=Distance('location', point))

        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')
        if start_time and end_time:
            queryset = queryset.exclude(
                reservations__start_time__lt=end_time,
                reservations__end_time__gt=start_time
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)




class FootballFieldDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FootballField.objects.all()
    serializer_class = FootballFieldSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, UpdateDeletePermission]


class ReservationListCreateView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_field_owner:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, DeletePersonalObjectPermission]

class UserStatsView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        # user = get_object_or_404(User, id=4)

        total_spent = Reservation.objects.filter(user=user).aggregate(
            total=Sum('total_price')
        )['total'] or 0

        most_visited_field = FootballField.objects.filter(reservations__user=user).annotate(
            visit_count=Count('reservations')
        ).order_by('-visit_count').first()

        return Response({
            'total_spent': total_spent,
            'reservation_count': user.reservations.count(),
            'most_visited_field': most_visited_field.name if most_visited_field else None,
        })

class FieldOwnerStatsView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        # user = get_object_or_404(User, id=4)

        if not user.is_field_owner:
            return Response({"error": "User is not a field owner"}, status=400)

        fields = user.fields.all()
        total_revenue = Reservation.objects.filter(field__in=fields).aggregate(
            total=Sum('total_price')
        )['total'] or 0

        most_popular_field = fields.annotate(
            reservation_count=Count('reservations')
        ).order_by('-reservation_count').first()

        return Response({
            'total_revenue': total_revenue,
            'field_count': fields.count(),
            'most_popular_field': most_popular_field.name if most_popular_field else None,
        })

class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)