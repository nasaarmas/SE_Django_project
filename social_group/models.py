from django.db import models
from django.conf import settings


class SocialGroupMember(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('member', 'Member'),
    )
    social_group = models.ForeignKey('SocialGroup', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='social_group_members', on_delete=models.CASCADE, null=False,
                             blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_left = models.DateTimeField(null=True, blank=True)
    role = models.CharField(max_length=50, null=False, blank=False, choices=ROLE_CHOICES)


class SocialGroup(models.Model):
    PRIVACY_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
    )

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    privacy = models.CharField(max_length=7, choices=PRIVACY_CHOICES, default='public')


class SocialGroupPost(models.Model):
    social_group = models.ForeignKey(SocialGroup, related_name='posts', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='social_group_posts', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    media = models.FileField(upload_to='social_group_posts/', null=True, blank=True)

    def __str__(self):
        return f"Post by {self.user.first_name} {self.user.last_name} in {self.social_group.name} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(SocialGroupPost, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.get_full_name()} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['created_at']


class SocialGroupEvent(models.Model):
    TOURNAMENT_CHOICES = (
        ('no', 'No Tournament'),
        ('individual', 'Individual Tournament'),
        ('team', 'Team Tournament'),
    )

    social_group = models.ForeignKey('SocialGroup', related_name='events', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2,
                                 default=0.00)  # Możesz dostosować max_digits i decimal_places
    sponsors = models.TextField(blank=True, null=True)  # Długi string do przechowywania informacji o sponsorach
    is_tournament = models.CharField(max_length=10, choices=TOURNAMENT_CHOICES, default='no')

    def __str__(self):
        return f"{self.name} in {self.social_group.name}"

    class Meta:
        ordering = ['-id']  # Zakładam, że chcesz sortować wydarzenia według najnowszych. Możesz to zmienić.


class SocialGroupEventMember(models.Model):
    ROLE_CHOICES = (
        ('participant', 'Participant'),
        ('organizer', 'Organizer'),
        ('spectator', 'Spectator'),
    )

    event = models.ForeignKey(SocialGroupEvent, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='event_memberships', on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role} in {self.event.name}"

