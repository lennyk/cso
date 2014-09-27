# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=2)),
                ('college_name', models.CharField(max_length=60)),
                ('latin_dance_organization_name', models.CharField(max_length=60)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CollegeCSOAttendance',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('attending', models.BooleanField(default=False)),
                ('performing', models.BooleanField(default=False)),
                ('competing', models.BooleanField(default=False)),
                ('college', models.ForeignKey(to='events.College')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CollegeURL',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('url_type', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('college', models.ForeignKey(to='events.College')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField(null=True, blank=True)),
                ('title', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=500)),
                ('information', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
