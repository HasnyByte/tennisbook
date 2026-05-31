from django import template
from booking.models import Court, Booking

register = template.Library()


@register.simple_tag
def get_total_courts():
    return Court.objects.count()


@register.simple_tag
def get_available_courts():
    return Court.objects.filter(is_available=True).count()


@register.simple_tag
def get_total_bookings():
    return Booking.objects.count()


@register.simple_tag
def get_pending_bookings():
    return Booking.objects.filter(status='pending').count()
