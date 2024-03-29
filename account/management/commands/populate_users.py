from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from account.models import User
from location.models import City

class Command(BaseCommand):
    help = 'Populates the database with fake users'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--number', type=int, default=100, help='Number of fake users to create')

    def handle(self, *args, **options):
        number = options['number']
        fake = Faker()

        with transaction.atomic():
            for _ in range(number):
                city_name = fake.city()
                city, _ = City.objects.get_or_create(name=city_name)

                User.objects.create_user(
                    email=fake.unique.email(),
                    password='password',  # You might want to use a more secure password or generate one dynamically
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    gender=fake.random_element(elements=('MALE', 'FEMALE')),
                    date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=90),
                    city=city,
                    email_activated=fake.boolean(),
                    terms_accepted=fake.boolean(),
                    terms_accepted_date=fake.past_datetime(start_date="-2y", tzinfo=None) if fake.boolean() else None,
                    status_type=fake.random_element(elements=('online', 'away', 'busy', 'offline', 'do_not_disturb', 'be_right_back')),
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {number} fake users.'))
