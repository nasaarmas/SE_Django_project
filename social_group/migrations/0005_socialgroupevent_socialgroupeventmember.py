# Generated by Django 4.0.10 on 2024-02-03 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social_group', '0004_remove_socialgroupmember_is_invited'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialGroupEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('budget', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('sponsors', models.TextField(blank=True, null=True)),
                ('is_tournament', models.CharField(choices=[('no', 'No Tournament'), ('individual', 'Individual Tournament'), ('team', 'Team Tournament')], default='no', max_length=10)),
                ('social_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='social_group.socialgroup')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SocialGroupEventMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('role', models.CharField(choices=[('participant', 'Participant'), ('organizer', 'Organizer'), ('spectator', 'Spectator')], max_length=50)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='social_group.socialgroupevent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_memberships', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]