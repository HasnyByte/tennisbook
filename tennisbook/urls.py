from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "TennisBook Admin"
admin.site.site_title = "TennisBook"
admin.site.index_title = "Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booking.urls')),
]
