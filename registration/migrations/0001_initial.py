# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollegeVerificationMessage',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('message', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(help_text="We will sign you in at the event with your driver's license or other ID card so enter your first and last name exactly as it appears on your ID card.", max_length=30)),
                ('college_affiliated', models.BooleanField(default=False, choices=[(False, 'I do not belong to a college dance club or team.'), (True, 'I am an active member of a college dance club or team.')])),
                ('college_verification_type', models.CharField(blank=True, help_text='If you have a .edu email address, please use the email address verification option. If you do not have a .edu email address but are an active member of a college dance club or team (coach, alumni, etc.) please choose the message option and provide a brief explanation.', null=True, default='email', max_length=12, choices=[('email', 'Verify by using a .edu email address.'), ('message', 'Verify by providing a written message.')])),
                ('partner_type', models.CharField(max_length=2, verbose_name='dance orientation', choices=[('LD', 'Lead'), ('FW', 'Follow')])),
                ('college_group', models.ForeignKey(blank=True, to='events.College', null=True, default=None)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SavedCustomer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('stripe_id', models.CharField(max_length=50, unique=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('charge_id', models.CharField(max_length=50, unique=True)),
                ('registration', models.OneToOneField(to='registration.Registration')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='collegeverificationmessage',
            name='registration',
            field=models.OneToOneField(to='registration.Registration'),
            preserve_default=True,
        ),
    ]
