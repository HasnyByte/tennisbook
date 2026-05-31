from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Booking, Court

INPUT_CLASS = 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-100 transition-all font-body text-gray-800'

ADMIN_INPUT_CLASS = 'w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-100 transition-all text-sm text-gray-800 bg-white'


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'phone', 'booking_date', 'booking_hour', 'notes']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Enter your email address'}),
            'phone': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Enter your phone number'}),
            'booking_date': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'booking_hour': forms.Select(attrs={'class': INPUT_CLASS + ' bg-white'}),
            'notes': forms.Textarea(attrs={'class': INPUT_CLASS, 'rows': 3, 'placeholder': 'Additional notes (optional)'}),
        }


class CourtForm(forms.ModelForm):
    class Meta:
        model = Court
        fields = ['name', 'description', 'price_per_hour', 'location', 'is_available', 'image_url', 'facilities']
        widgets = {
            'name': forms.TextInput(attrs={'class': ADMIN_INPUT_CLASS, 'placeholder': 'Nama lapangan'}),
            'description': forms.Textarea(attrs={'class': ADMIN_INPUT_CLASS, 'rows': 3, 'placeholder': 'Deskripsi lapangan'}),
            'price_per_hour': forms.NumberInput(attrs={'class': ADMIN_INPUT_CLASS, 'placeholder': '0.00', 'step': '0.01'}),
            'location': forms.TextInput(attrs={'class': ADMIN_INPUT_CLASS, 'placeholder': 'Lokasi lapangan'}),
            'image_url': forms.URLInput(attrs={'class': ADMIN_INPUT_CLASS, 'placeholder': 'https://...'}),
            'facilities': forms.CheckboxSelectMultiple(),
            'is_available': forms.CheckboxInput(attrs={'class': 'w-4 h-4 rounded border-gray-300 text-green-600 focus:ring-green-500'}),
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Enter your email address'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': INPUT_CLASS, 'placeholder': 'Choose a username'})
        self.fields['password1'].widget.attrs.update({'class': INPUT_CLASS, 'placeholder': 'Create a password'})
        self.fields['password2'].widget.attrs.update({'class': INPUT_CLASS, 'placeholder': 'Confirm your password'})
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': INPUT_CLASS, 'placeholder': 'Enter your username'})
        self.fields['password'].widget.attrs.update({'class': INPUT_CLASS, 'placeholder': 'Enter your password'})
