# Generated by Django 3.1 on 2021-04-06 11:56

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Garrisons', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('last_session_key', models.CharField(blank=True, max_length=40, null=True)),
                ('has_valid_password', models.BooleanField(default=False, verbose_name='Has valid password')),
                ('last_password_change', models.DateTimeField(blank=True, null=True, verbose_name='Last password change')),
                ('last_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='Last IP')),
                ('is_logged_in', models.BooleanField(default=False, verbose_name='Logged in')),
                ('last_logout', models.DateTimeField(blank=True, null=True, verbose_name='Last logout')),
                ('garrison', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin_user', to='Garrisons.garrison', verbose_name='Garrison')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('personal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Garrisons.personal', verbose_name='Personal')),
                ('soldier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Garrisons.soldier', verbose_name='Soldier')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CustomLogger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=500, verbose_name='Action')),
                ('user', models.CharField(max_length=500, verbose_name='User')),
                ('action_flag', models.PositiveSmallIntegerField(choices=[(1, 'Addition'), (2, 'Change'), (3, 'Deletion'), (4, 'Log in/Log out')], verbose_name='action flag')),
                ('event_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Event Date')),
                ('object_type', models.CharField(default='', max_length=250, verbose_name='Object Type')),
                ('object_link', models.CharField(blank=True, max_length=250, null=True, verbose_name='Object URL')),
            ],
            options={
                'verbose_name': 'Log Entry',
                'verbose_name_plural': 'Log Entries',
            },
        ),
        migrations.CreateModel(
            name='LoginFailedIP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(verbose_name='IP')),
                ('tries', models.PositiveSmallIntegerField(verbose_name='Try Count')),
                ('last_try', models.DateTimeField(auto_now=True, verbose_name='Last Try')),
            ],
        ),
        migrations.CreateModel(
            name='UserPassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=100, verbose_name='Password')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
