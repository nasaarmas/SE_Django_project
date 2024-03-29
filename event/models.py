from django.db import models
from account.models import User
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=255)
    begin_ts = models.DateTimeField(default=timezone.now)
    end_ts = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=255)
    expenses = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()

    def __str__(self):
        return self.title


class EventMember(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('guest', 'Guest'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    member = models.ForeignKey(User, related_name='event_members', on_delete=models.CASCADE, null=False, blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_left = models.DateTimeField(null=True, blank=True)
    role = models.CharField(max_length=50, null=False, blank=False, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.member} - {self.event.title}"
