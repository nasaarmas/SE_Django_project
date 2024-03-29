# events/views.py
from rest_framework import viewsets
from .models import Event, EventMember
from .serializers import EventSerializer, EventMemberSerializer
from rest_framework.response import Response


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventMemberViewSet(viewsets.ModelViewSet):
    serializer_class = EventMemberSerializer

    def get_queryset(self):
        # Filter the queryset based on the event_id in the URL
        return EventMember.objects.filter(event_id=self.kwargs['event_id'])
