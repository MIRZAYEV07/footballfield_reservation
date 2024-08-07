
from django.contrib import admin
from .models import FootballField, FieldImage, Reservation


class FieldImageInline(admin.TabularInline):
    model = FieldImage
    extra = 1

@admin.register(FootballField)
class FootballFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'price_per_hour', 'owner')
    list_filter = ('owner',)
    search_fields = ('name', 'address')
    inlines = [FieldImageInline]

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('field', 'user', 'start_time', 'end_time')
    list_filter = ('field', 'user')
    search_fields = ('field__name', 'user__username')
    date_hierarchy = 'start_time'
