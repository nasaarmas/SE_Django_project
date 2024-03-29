from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from account.models import User
from social_group.models import SocialGroup, SocialGroupMember, SocialGroupPost

class Command(BaseCommand):
    help = 'Populates the database with fake social groups, members, and posts'

    def add_arguments(self, parser):
        parser.add_argument('-g', '--groups', type=int, default=10, help='Number of fake social groups to create')
        parser.add_argument('-p', '--posts', type=int, default=5, help='Number of fake posts per social group')

    def handle(self, *args, **options):
        groups_count = options['groups']
        posts_count = options['posts']
        fake = Faker()

        with transaction.atomic():
            for _ in range(groups_count):
                social_group = SocialGroup.objects.create(
                    name=fake.unique.company(),
                    description=fake.catch_phrase(),
                )

                users = User.objects.all()
                for user in users:
                    SocialGroupMember.objects.create(
                        social_group=social_group,
                        user=user,
                        role=fake.random_element(elements=('admin', 'member', 'guest')),
                    )

                for _ in range(posts_count):
                    post_user = fake.random_element(elements=users)
                    SocialGroupPost.objects.create(
                        social_group=social_group,
                        user=post_user,
                        content=fake.text(max_nb_chars=500),  # Adjust text length as needed
                        # media field is optional, adjust as needed
                    )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {groups_count} fake social groups with {posts_count} posts each.'))
