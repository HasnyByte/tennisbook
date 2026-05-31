from django.contrib import admin
from .models import Court, Facility, Booking


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_per_hour', 'location', 'is_available', 'created_at']
    list_filter = ['is_available']
    search_fields = ['name', 'location']
    filter_horizontal = ['facilities']
    list_editable = ['is_available']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'court', 'booking_date', 'booking_hour', 'status', 'user', 'created_at']
    list_filter = ['status', 'booking_date', 'court']
    search_fields = ['full_name', 'email', 'phone']
    list_editable = ['status']
    readonly_fields = ['created_at']
    autocomplete_fields = []
