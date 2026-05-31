from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from booking.models import Court, Facility


class Command(BaseCommand):
    help = 'Seed the database with sample courts, facilities, and admin user'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # Admin User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(username='admin', password='admin123', email='admin@tennisbook.id')
            self.stdout.write(self.style.SUCCESS('Admin user created: admin / admin123'))
        else:
            self.stdout.write('Admin already exists, skipping.')

        # Sample user for testing
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user(username='testuser', password='test1234', email='test@tennisbook.id', first_name='Test', last_name='User')
            self.stdout.write(self.style.SUCCESS('Test user created: testuser / test1234'))

        # Facilities
        locker, _ = Facility.objects.get_or_create(name='Locker Room', defaults={'description': 'Secure locker rooms with shower facilities.'})
        parking, _ = Facility.objects.get_or_create(name='Parking Area', defaults={'description': 'Free dedicated parking for all visitors.'})
        cafe, _ = Facility.objects.get_or_create(name='Cafeteria', defaults={'description': 'On-site cafeteria with drinks and snacks.'})
        self.stdout.write(self.style.SUCCESS('Facilities created.'))

        courts_data = [
            {
                'name': 'Grand Slam Arena',
                'description': 'Our flagship hard court with professional-grade surface used in international tournaments. Features spectator seating, floodlights for evening play, and freshly painted lines.',
                'price_per_hour': 150000,
                'location': 'Level 1, TennisBook Main Complex, Jakarta Selatan',
                'is_available': True,
                'image_url': 'https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=800&q=80',
                'facilities': [locker, parking, cafe],
            },
            {
                'name': 'Clay Court Classic',
                'description': 'Premium red clay court modeled after the Roland Garros surface. Perfect for baseline players. The clay surface reduces impact on joints.',
                'price_per_hour': 120000,
                'location': 'Level 2, TennisBook Main Complex, Jakarta Selatan',
                'is_available': True,
                'image_url': 'https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?w=800&q=80',
                'facilities': [locker, parking],
            },
            {
                'name': 'Wimbledon Grass Court',
                'description': 'Experience the prestige of playing on genuine grass. Freshly maintained turf provides an authentic traditional tennis feel.',
                'price_per_hour': 130000,
                'location': 'Outdoor Wing A, TennisBook Sports Park, Jakarta Timur',
                'is_available': True,
                'image_url': 'https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=800&q=80',
                'facilities': [parking, cafe],
            },
            {
                'name': 'Indoor Pro Court',
                'description': 'Fully air-conditioned indoor hard court with synthetic cushioned surface. Perfect for year-round play regardless of weather.',
                'price_per_hour': 80000,
                'location': 'TennisBook Indoor Arena, Jakarta Barat',
                'is_available': False,
                'image_url': 'https://images.unsplash.com/photo-1545809074-59472b3f5ecc?w=800&q=80',
                'facilities': [locker, parking],
            },
        ]

        for data in courts_data:
            facilities = data.pop('facilities')
            court, created = Court.objects.get_or_create(name=data['name'], defaults=data)
            if created:
                court.facilities.set(facilities)
                self.stdout.write(self.style.SUCCESS(f'Court created: {court.name}'))
            else:
                self.stdout.write(f'Court already exists: {court.name}')

        self.stdout.write(self.style.SUCCESS('\nSeeding complete!'))
        self.stdout.write('Admin: http://127.0.0.1:8000/admin/  |  admin / admin123')
        self.stdout.write('Test user: testuser / test1234')
