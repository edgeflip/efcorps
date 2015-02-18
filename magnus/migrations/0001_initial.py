# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magnus.models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('campaign_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Campaign Name')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'campaigns',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Client Name')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'clients',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientAppUser',
            fields=[
                ('client_app_user_id', models.AutoField(serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'client_app_users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.AutoField(serialize=False, primary_key=True)),
                ('event_type', models.CharField(max_length=64, verbose_name=b'Event Type')),
                ('event_datetime', models.DateTimeField(db_index=True)),
                ('data', magnus.models.JSONField()),
                ('campaign', models.ForeignKey(to='magnus.Campaign')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
                'db_table': 'events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FBApp',
            fields=[
                ('appid', models.BigIntegerField(serialize=False, verbose_name=b'FB App ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name=b'FB App Namespace')),
                ('secret', models.CharField(max_length=32, verbose_name=b'FB App Secret')),
                ('api', models.DecimalField(default=Decimal('2.2'), verbose_name=b'FB API Version', max_digits=3, decimal_places=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('name',),
                'db_table': 'fb_apps',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FBAppUser',
            fields=[
                ('app_user_id', models.AutoField(serialize=False, primary_key=True)),
                ('asid', models.BigIntegerField(verbose_name=b'App-scoped ID', db_index=True)),
                ('app', models.ForeignKey(to='magnus.FBApp')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'fb_app_users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FBPermission',
            fields=[
                ('code', models.SlugField(max_length=64, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('code',),
                'db_table': 'fb_permissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FBUserToken',
            fields=[
                ('user_token_id', models.AutoField(serialize=False, primary_key=True)),
                ('access_token', models.TextField(unique=True, verbose_name=b'Access Token')),
                ('expiration', models.DateTimeField()),
                ('app_user', models.ForeignKey(to='magnus.FBAppUser')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'fb_user_tokens',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('efid', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Person Name', db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'persons',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('visit_id', models.AutoField(serialize=False, primary_key=True)),
                ('session_id', models.CharField(max_length=40, db_index=True)),
                ('app_id', models.BigIntegerField(db_column=b'appid')),
                ('ip', models.GenericIPAddressField()),
                ('user_agent', models.CharField(default=b'', max_length=1028, blank=True)),
                ('referer', models.CharField(default=b'', max_length=1028, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'visits',
                'get_latest_by': 'created',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('visitor_id', models.AutoField(serialize=False, primary_key=True)),
                ('uuid', models.CharField(unique=True, max_length=40)),
                ('fbid', models.BigIntegerField(unique=True, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'visitors',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='visit',
            name='visitor',
            field=models.ForeignKey(related_name='visits', to='magnus.Visitor'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='visit',
            unique_together=set([('session_id', 'app_id')]),
        ),
        migrations.AddField(
            model_name='fbappuser',
            name='person',
            field=models.ForeignKey(to='magnus.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fbapp',
            name='permissions',
            field=models.ManyToManyField(to='magnus.FBPermission', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='visit',
            field=models.ForeignKey(to='magnus.Visit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientappuser',
            name='app_user',
            field=models.ForeignKey(to='magnus.FBAppUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientappuser',
            name='client',
            field=models.ForeignKey(to='magnus.Client'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='client',
            field=models.ForeignKey(to='magnus.Client'),
            preserve_default=True,
        ),
    ]
