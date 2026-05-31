
  TENNISBOOK — Book Your Tennis Court Easily
  Django Web Application | College Assignment Project
================================================================================

DESCRIPTION
-----------
TennisBook is a tennis court booking web application built with Django.
It allows users to browse available tennis courts, view court details,
and submit booking requests. Admins manage courts, bookings, and facilities
via the Django Admin dashboard.

TECH STACK
----------
- Backend    : Django 4.2 (Python)
- Database   : SQLite (auto-generated, no setup required)
- Frontend   : Tailwind CSS CDN + Font Awesome 6.4
- Fonts      : Google Fonts (Anton, Bebas Neue, Inter)
- Images     : Unsplash CDN (no authentication required)
- Python     : 3.10+

PROJECT STRUCTURE
-----------------
tennisbook/
  manage.py
  requirements.txt
  README.md
  db.sqlite3                        (auto-generated on migrate)
  tennisbook/                       (project config)
    __init__.py
    settings.py
    urls.py
    wsgi.py
  booking/                          (main app)
    __init__.py
    admin.py
    apps.py
    forms.py
    models.py
    urls.py
    views.py
    management/
      __init__.py
      commands/
        __init__.py
        seed_data.py
    templates/
      base.html
      home.html
      service.html
      court_list.html
      court_detail.html
      booking_form.html
      booking_success.html
      contact.html

INSTALLATION
------------

1. Clone or download the project:
   git clone <repo-url>
   cd tennisbook

2. Create a virtual environment:
   python -m venv venv

3. Activate the virtual environment:
   Linux/Mac:  source venv/bin/activate
   Windows:    venv\Scripts\activate

4. Install dependencies:
   pip install -r requirements.txt

5. Run database migrations:
   python manage.py migrate

6. Seed sample data (courts, facilities, admin user):
   python manage.py seed_data

7. (Optional) Create a custom superuser:
   python manage.py createsuperuser

8. Start the development server:
   python manage.py runserver

9. Open in browser:
   http://127.0.0.1:8000/

DEFAULT ADMIN CREDENTIALS
--------------------------
Username : admin
Password : admin123
URL      : http://127.0.0.1:8000/admin/

NOTE: Change the password immediately in a production environment.

PAGES AND URLS
--------------
/                        Home page with hero and featured courts
/courts/                 Full court listing page
/courts/<id>/            Court detail page
/courts/<id>/book/       Booking form page
/booking/success/        Booking success confirmation page
/service/                Services information page
/contact/                Contact page
/admin/                  Django Admin dashboard (login required)
/admin/login/            Admin login page

MODELS
------
Court
  - name          (CharField)      : Court display name
  - description   (TextField)      : Detailed court description
  - price_per_hour(DecimalField)   : Hourly rate in IDR
  - location      (CharField)      : Physical court location
  - is_available  (BooleanField)   : Court availability toggle
  - image_url     (URLField)       : Unsplash image URL
  - facilities    (ManyToManyField): Associated facilities
  - created_at    (DateTimeField)  : Record creation timestamp

Facility
  - name          (CharField)      : Facility name (e.g. Locker Room)
  - description   (TextField)      : Optional description

Booking
  - court         (ForeignKey)     : Related court
  - full_name     (CharField)      : Customer full name
  - email         (EmailField)     : Customer email
  - phone         (CharField)      : Customer phone number
  - booking_date  (DateField)      : Date of booking
  - booking_hour  (CharField)      : Hour slot (06:00 - 22:00)
  - notes         (TextField)      : Optional additional notes
  - status        (CharField)      : pending / confirmed / cancelled
  - created_at    (DateTimeField)  : Record creation timestamp

HOW TO ADD SAMPLE COURTS VIA ADMIN
------------------------------------
1. Log in at http://127.0.0.1:8000/admin/
2. Go to Facilities and add: Locker Room, Parking Area, Cafeteria
3. Go to Courts and add courts with:
   - Name, description, price, location
   - image_url: paste any Unsplash URL
   - Select facilities using the horizontal filter
4. Go to Bookings to view and manage all reservations

NOTES
-----
- No emoji in UI, templates, or README
- All styling via Tailwind CSS CDN (no build step required)
- Database is SQLite (db.sqlite3), auto-created on first migrate
- The project is intended as a college assignment demonstration
- DEBUG=True and ALLOWED_HOSTS=['*'] are set for local development only
- Do not deploy with these settings to production
