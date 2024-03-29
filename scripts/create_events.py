import json
from datetime import datetime
from django.utils import timezone
from account.models import User
from event.models import Event, EventMember

with open('scripts/dataset/ex_events.json') as f:
    events_data = json.load(f)

for event_data in events_data:
    event = Event.objects.create(
        title=event_data['title'],
        begin_ts=datetime.fromisoformat(event_data['begin_ts']).astimezone(timezone.utc),
        end_ts=datetime.fromisoformat(event_data['end_ts']).astimezone(timezone.utc),
        location=event_data['location'],
        expenses=float(event_data['expenses']),
        details=event_data['details']
    )

    for member_data in event_data['members']:
        user = User.objects.get(id=member_data['user_id'])
        EventMember.objects.create(
            event=event,
            member=user,
            role=member_data['role']
        )
