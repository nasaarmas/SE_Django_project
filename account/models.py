from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from social_group.models import SocialGroup
from location.models import City


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    # Basic information about user
    id = models.AutoField(primary_key=True, db_index=True)
    username = None
    email = models.EmailField(_('Email address'), unique=True)
    email_activated = models.BooleanField(default=False, blank=True)
    first_name = models.CharField(max_length=64, blank=False, null=False)
    last_name = models.CharField(max_length=128, blank=False, null=False)
    gender = models.CharField(
        max_length=6,
        choices=(('MALE', 'Male'),
                 ('FEMALE', 'Female')),
        blank=True,
        null=True,
    )
    date_of_birth = models.DateField(null=True, blank=True, db_index=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True)

    status_type = models.CharField(
        max_length=16,
        choices=(
            ('online', 'Online'),
            ('away', 'Away'),
            ('busy', 'Busy'),
            ('offline', 'Offline'),
            ('do_not_disturb', 'Do Not Disturb'),
            ('be_right_back', 'Be Right Back'),
        ),
        blank=False,
        null=False,
        default='online'
    )
    # terms issues
    terms_accepted = models.BooleanField(default=True, blank=True)
    terms_accepted_date = models.DateTimeField(blank=True, null=True, verbose_name='Terms consent date')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name',
                       'last_name',
                       'gender',
                       'date_of_birth', ]

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    sg_id = models.ForeignKey(SocialGroup, on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_invitation = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.email}: {self.message}"
