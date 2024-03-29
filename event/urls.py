from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EventMemberViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='events')
router.register(r'events/(?P<event_id>[^/.]+)/members', EventMemberViewSet, basename='event-members')

urlpatterns = [
    path('', include(router.urls)),
]
