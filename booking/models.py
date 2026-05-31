from django.db import models
from django.conf import settings


class Facility(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Facilities"


class Court(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=300)
    is_available = models.BooleanField(default=True)
    image_url = models.URLField(
        blank=True,
        default="https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=800&q=80"
    )
    facilities = models.ManyToManyField(Facility, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
]

HOUR_CHOICES = [(f"{h:02d}:00", f"{h:02d}:00") for h in range(6, 23)]


class Booking(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings'
    )
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    booking_date = models.DateField()
    booking_hour = models.CharField(max_length=10, choices=HOUR_CHOICES)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.court.name} - {self.booking_date}"

    class Meta:
        ordering = ['-created_at']
