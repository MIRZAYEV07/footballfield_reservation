import django_filters
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from field.models import FootballField


class AvailableFieldFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(method='filter_available')
    end_time = django_filters.DateTimeFilter(method='filter_available')
    name = django_filters.CharFilter(lookup_expr='icontains')
    address = django_filters.CharFilter(lookup_expr='icontains')
    latitude = django_filters.NumberFilter(method='filter_distance', label='Latitude')
    longitude = django_filters.NumberFilter(method='filter_distance', label='Longitude')

    class Meta:
        model = FootballField
        fields = ['name', 'address', 'start_time', 'end_time', 'latitude', 'longitude']

    def filter_available(self, queryset, name, value):
        if name == 'start_time':
            return queryset.exclude(reservations__end_time__gt=value, reservations__start_time__lte=value)
        elif name == 'end_time':
            return queryset.exclude(reservations__start_time__lt=value, reservations__end_time__gte=value)
        return queryset

    def filter_distance(self, queryset, name, value):
        latitude = self.data.get('latitude')
        longitude = self.data.get('longitude')
        if latitude and longitude:
            point = Point(float(longitude), float(latitude), srid=4326)
            return queryset.annotate(distance=Distance('location', point)).order_by('distance')
        return queryset