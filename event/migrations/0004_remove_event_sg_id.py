# Generated by Django 4.0.10 on 2024-02-03 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_event_sg_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='sg_id',
        ),
    ]
