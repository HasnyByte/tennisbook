from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('service/', views.service, name='service'),
    path('courts/', views.court_list, name='court_list'),
    path('courts/<int:pk>/', views.court_detail, name='court_detail'),
    path('courts/<int:pk>/book/', views.booking_form, name='booking_form'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),

    # Custom Admin Panel
    path('panel/', views.custom_admin_dashboard, name='custom_admin_dashboard'),

    # Booking CRUD
    path('panel/bookings/', views.admin_booking_list, name='admin_booking_list'),
    path('panel/bookings/<int:pk>/edit/', views.admin_booking_edit, name='admin_booking_edit'),
    path('panel/bookings/<int:pk>/delete/', views.admin_booking_delete, name='admin_booking_delete'),
    path('panel/bookings/<int:pk>/status/', views.admin_booking_update_status, name='admin_booking_update_status'),

    # Court CRUD
    path('panel/courts/', views.admin_court_list, name='admin_court_list'),
    path('panel/courts/add/', views.admin_court_add, name='admin_court_add'),
    path('panel/courts/<int:pk>/edit/', views.admin_court_edit, name='admin_court_edit'),
    path('panel/courts/<int:pk>/delete/', views.admin_court_delete, name='admin_court_delete'),
]
