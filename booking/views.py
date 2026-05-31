from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from .models import Court, Booking, Facility
from .forms import BookingForm, UserRegisterForm, UserLoginForm, CourtForm


def home(request):
    courts = Court.objects.filter(is_available=True)[:3]
    return render(request, 'home.html', {'courts': courts})


def service(request):
    return render(request, 'service.html')


def court_list(request):
    courts = Court.objects.all()
    return render(request, 'court_list.html', {'courts': courts})


def court_detail(request, pk):
    court = get_object_or_404(Court, pk=pk)
    facilities = court.facilities.all()
    return render(request, 'court_detail.html', {'court': court, 'facilities': facilities})


def booking_form(request, pk):
    court = get_object_or_404(Court, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.court = court
            booking.status = 'pending'
            if request.user.is_authenticated:
                booking.user = request.user
            booking.save()
            return redirect('booking_success')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['full_name'] = request.user.get_full_name() or request.user.username
            initial['email'] = request.user.email
        form = BookingForm(initial=initial)
    return render(request, 'booking_form.html', {'form': form, 'court': court})


def booking_success(request):
    return render(request, 'booking_success.html')


def contact(request):
    return render(request, 'contact.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created! Welcome, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required(login_url='/login/')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('court')
    return render(request, 'my_bookings.html', {'bookings': bookings})


# ─── Admin Panel (Custom) ────────────────────────────────────────────────────

def is_staff(user):
    return user.is_staff

staff_required = user_passes_test(is_staff, login_url='/login/')


@login_required(login_url='/login/')
@staff_required
def custom_admin_dashboard(request):
    total_courts = Court.objects.count()
    available_courts = Court.objects.filter(is_available=True).count()
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    cancelled_bookings = Booking.objects.filter(status='cancelled').count()
    recent_bookings = Booking.objects.select_related('court').order_by('-created_at')[:5]
    context = {
        'total_courts': total_courts,
        'available_courts': available_courts,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'custom_admin/dashboard.html', context)


# ─── Booking CRUD ─────────────────────────────────────────────────────────────

@login_required(login_url='/login/')
@staff_required
def admin_booking_list(request):
    status_filter = request.GET.get('status', '')
    bookings = Booking.objects.select_related('court', 'user').order_by('-created_at')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    context = {'bookings': bookings, 'status_filter': status_filter}
    return render(request, 'custom_admin/booking_list.html', context)


@login_required(login_url='/login/')
@staff_required
def admin_booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        status = request.POST.get('status', booking.status)
        if form.is_valid():
            b = form.save(commit=False)
            b.status = status
            b.save()
            messages.success(request, f'Booking #{pk} berhasil diperbarui.')
            return redirect('admin_booking_list')
        else:
            messages.error(request, 'Terdapat kesalahan pada form.')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'custom_admin/booking_edit.html', {'form': form, 'booking': booking})


@login_required(login_url='/login/')
@staff_required
def admin_booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        name = str(booking)
        booking.delete()
        messages.success(request, f'Booking "{name}" berhasil dihapus.')
        return redirect('admin_booking_list')
    return render(request, 'custom_admin/confirm_delete.html', {
        'object': booking,
        'object_type': 'Booking',
        'cancel_url': 'admin_booking_list',
    })


@login_required(login_url='/login/')
@staff_required
def admin_booking_update_status(request, pk):
    """AJAX endpoint to quickly update booking status."""
    if request.method == 'POST':
        booking = get_object_or_404(Booking, pk=pk)
        new_status = request.POST.get('status')
        if new_status in ['pending', 'confirmed', 'cancelled']:
            booking.status = new_status
            booking.save()
            return JsonResponse({'success': True, 'status': new_status})
    return JsonResponse({'success': False}, status=400)


# ─── Court CRUD ───────────────────────────────────────────────────────────────

@login_required(login_url='/login/')
@staff_required
def admin_court_list(request):
    courts = Court.objects.prefetch_related('facilities').order_by('-created_at')
    return render(request, 'custom_admin/court_list.html', {'courts': courts})


@login_required(login_url='/login/')
@staff_required
def admin_court_add(request):
    if request.method == 'POST':
        form = CourtForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lapangan baru berhasil ditambahkan.')
            return redirect('admin_court_list')
        else:
            messages.error(request, 'Terdapat kesalahan pada form.')
    else:
        form = CourtForm()
    return render(request, 'custom_admin/court_form.html', {'form': form, 'action': 'Tambah'})


@login_required(login_url='/login/')
@staff_required
def admin_court_edit(request, pk):
    court = get_object_or_404(Court, pk=pk)
    if request.method == 'POST':
        form = CourtForm(request.POST, instance=court)
        if form.is_valid():
            form.save()
            messages.success(request, f'Lapangan "{court.name}" berhasil diperbarui.')
            return redirect('admin_court_list')
        else:
            messages.error(request, 'Terdapat kesalahan pada form.')
    else:
        form = CourtForm(instance=court)
    return render(request, 'custom_admin/court_form.html', {'form': form, 'action': 'Edit', 'court': court})


@login_required(login_url='/login/')
@staff_required
def admin_court_delete(request, pk):
    court = get_object_or_404(Court, pk=pk)
    if request.method == 'POST':
        name = court.name
        court.delete()
        messages.success(request, f'Lapangan "{name}" berhasil dihapus.')
        return redirect('admin_court_list')
    return render(request, 'custom_admin/confirm_delete.html', {
        'object': court,
        'object_type': 'Lapangan',
        'cancel_url': 'admin_court_list',
    })
