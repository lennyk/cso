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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('city', models.CharField(max_length=60)),
                ('state', models.CharField(default='CA', max_length=2)),
                ('college_name', models.CharField(max_length=80)),
                ('latin_dance_organization_name', models.CharField(max_length=80)),
                ('description', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CollegeCSOParticipation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('cso_year', models.IntegerField(default='2015', choices=[(2015, '2015')])),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('url_type', models.CharField(max_length=255, choices=[('facebook', 'Facebook'), ('website', 'Website'), ('youtube', 'YouTube')])),
                ('url', models.URLField()),
                ('college', models.ForeignKey(to='events.College')),
            ],
            options={
                'ordering': ['url_type'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=120)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='collegeurl',
            unique_together=set([('college', 'url_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='collegecsoparticipation',
            unique_together=set([('college', 'cso_year')]),
        ),
    ]
