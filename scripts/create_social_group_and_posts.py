# python3 manage.py shell < scripts/create_social_group.py
from django.core.management.base import BaseCommand
from faker import Faker
from social_group.models import SocialGroup, SocialGroupMember, SocialGroupPost
from account.models import User

fake = Faker()

# Create 5 social groups
for _ in range(5):
    group_name = fake.company()
    group_description = fake.catch_phrase()
    social_group = SocialGroup.objects.create(
        name=group_name,
        description=group_description
    )

    # Add all users to this social group
    users = User.objects.all()
    for user in users:
        SocialGroupMember.objects.create(
            social_group=social_group,
            user=user,
            role='member'
        )

    # Add 5 posts to this social group
    for _ in range(5):
        post_content = fake.text()
        post_user = fake.random_element(elements=users)
        SocialGroupPost.objects.create(
            social_group=social_group,
            user=post_user,
            content=post_content
        )
