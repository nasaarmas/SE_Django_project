import json
from datetime import datetime
from django.utils import timezone
from account.models import User
from social_group.models import SocialGroup, SocialGroupMember, SocialGroupPost

with open('scripts/dataset/ex_socialgroups.json') as f:
    data = json.load(f)

for item in data:
    social_group_data = item['social_group']
    group, created = SocialGroup.objects.get_or_create(name=social_group_data['name'],
                                                       description=social_group_data['description'])
    for member_data in item['members']:
        SocialGroupMember.objects.get_or_create(
            social_group=group,
            user=User.objects.get(id=member_data['user_id']),
            role=member_data['role']
        )

    for post_data in item['posts']:
        SocialGroupPost.objects.get_or_create(
            social_group=group,
            user=User.objects.get(id=post_data['user_id']),
            content=post_data['content']
        )
