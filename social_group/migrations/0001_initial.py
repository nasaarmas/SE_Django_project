# Generated by Django 4.0.10 on 2023-11-11 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialGroupPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('media', models.FileField(blank=True, null=True, upload_to='social_group_posts/')),
                ('social_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='social_group.socialgroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_group_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SocialGroupMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('date_left', models.DateTimeField(blank=True, null=True)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('member', 'Member'), ('guest', 'Guest')], max_length=50)),
                ('social_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_group.socialgroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_group_members', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
