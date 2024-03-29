# Generated by Django 4.2.6 on 2023-10-28 09:16

import account.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email address')),
                ('email_activated', models.BooleanField(blank=True, default=False)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=128)),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=6)),
                ('date_of_birth', models.DateField(blank=True, db_index=True, null=True)),
                ('status_type', models.CharField(choices=[('online', 'Online'), ('away', 'Away'), ('busy', 'Busy'), ('offline', 'Offline'), ('do_not_disturb', 'Do Not Disturb'), ('be_right_back', 'Be Right Back')], default='online', max_length=16)),
                ('terms_accepted', models.BooleanField(blank=True, default=True)),
                ('terms_accepted_date', models.DateTimeField(blank=True, null=True, verbose_name='Terms consent date')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='location.city')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', account.models.UserManager()),
            ],
        ),
    ]
