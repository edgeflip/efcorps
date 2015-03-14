# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FBApp'
        db.create_table('fb_apps', (
            ('fb_app_id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('namespace', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('current_api', self.gf('django.db.models.fields.DecimalField')(default='2.2', max_digits=3, decimal_places=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['FBApp'])

        # Adding M2M table for field current_permissions on 'FBApp'
        m2m_table_name = 'fb_apps_fb_permissions'
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('fbapp', models.ForeignKey(orm[u'magnus.fbapp'], null=False)),
            ('fbpermission', models.ForeignKey(orm[u'magnus.fbpermission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['fbapp_id', 'fbpermission_id'])

        # Adding model 'FBPermission'
        db.create_table('fb_permissions', (
            ('code', self.gf('django.db.models.fields.SlugField')(max_length=64, primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['FBPermission'])

        # Adding model 'FBAppUser'
        db.create_table('fb_app_users', (
            ('fb_app_user_id', self.gf('magnus.models.fields.BigSerialField')(primary_key=True)),
            ('fbid', self.gf('django.db.models.fields.BigIntegerField')()),
            ('fb_app', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fb_app_users', to=orm['magnus.FBApp'])),
            ('ef_user', self.gf('magnus.models.fields.FlexibleForeignKey')(related_name='fb_app_users', db_column='efid', to=orm['magnus.EFUser'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['FBAppUser'])

        # Adding unique constraint on 'FBAppUser', fields ['fbid', 'fb_app']
        db.create_unique('fb_app_users', ['fbid', 'fb_app_id'])

        # Adding unique constraint on 'FBAppUser', fields ['ef_user', 'fb_app']
        db.create_unique('fb_app_users', ['efid', 'fb_app_id'])

        # Adding model 'EFUser'
        db.create_table('ef_users', (
            ('efid', self.gf('magnus.models.fields.BigSerialField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254, unique=True, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['EFUser'])

        # Adding model 'FBUserToken'
        db.create_table('fb_user_tokens', (
            ('fb_user_token_id', self.gf('magnus.models.fields.BigSerialField')(primary_key=True)),
            ('fb_app_user', self.gf('magnus.models.fields.FlexibleForeignKey')(related_name='fb_user_tokens', to=orm['magnus.FBAppUser'])),
            ('access_token', self.gf('django.db.models.fields.TextField')()),
            ('expiration', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('api', self.gf('django.db.models.fields.DecimalField')(default='2.2', max_digits=3, decimal_places=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['FBUserToken'])

        # Adding unique constraint on 'FBUserToken', fields ['api', 'fb_app_user']
        db.create_unique('fb_user_tokens', ['api', 'fb_app_user_id'])

        # Adding model 'Campaign'
        db.create_table('campaigns', (
            ('campaign_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='campaigns', to=orm['magnus.Client'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['Campaign'])

        # Adding model 'Client'
        db.create_table('clients', (
            ('client_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('codename', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['Client'])

        # Adding model 'ClientFBAppUser'
        db.create_table('clients_fb_app_users', (
            ('client_app_user_id', self.gf('magnus.models.fields.BigSerialField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['magnus.Client'])),
            ('fb_app_user', self.gf('magnus.models.fields.FlexibleForeignKey')(related_name='+', to=orm['magnus.FBAppUser'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['ClientFBAppUser'])

        # Adding unique constraint on 'ClientFBAppUser', fields ['client', 'fb_app_user']
        db.create_unique('clients_fb_app_users', ['client_id', 'fb_app_user_id'])

        # Adding model 'Event'
        db.create_table('events', (
            ('event_id', self.gf('magnus.models.fields.BigSerialField')(primary_key=True)),
            ('visit', self.gf('magnus.models.fields.FlexibleForeignKey')(related_name='events', to=orm['magnus.Visit'])),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', null=True, to=orm['magnus.Campaign'])),
            ('event_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True)),
            ('data', self.gf('magnus.models.fields.JSONField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['Event'])

        # Adding model 'Visit'
        db.create_table('visits', (
            ('visit_id', self.gf('magnus.models.fields.BigSerialField')(primary_key=True)),
            ('visitor_agent', self.gf('magnus.models.fields.FlexibleForeignKey')(related_name='visits', to=orm['magnus.VisitorAgent'])),
            ('session_id', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('fb_app', self.gf('django.db.models.fields.related.ForeignKey')(related_name='visits', null=True, to=orm['magnus.FBApp'])),
            ('fbid', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('referer', self.gf('django.db.models.fields.CharField')(max_length=1028, blank=True)),
            ('source', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['Visit'])

        # Adding unique constraint on 'Visit', fields ['session_id', 'fb_app']
        db.create_unique('visits', ['session_id', 'fb_app_id'])

        # Adding model 'VisitorAgent'
        db.create_table('visitor_agents', (
            ('visitor_agent_id', self.gf('magnus.models.fields.BigSerialField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40, blank=True)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=1028, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['VisitorAgent'])

        # Adding model 'EFUserVisitorAgent'
        db.create_table('ef_users_visitor_agents', (
            ('ef_user_visitor_agent_id', self.gf('magnus.models.fields.BigSerialField')(primary_key=True)),
            ('ef_user', self.gf('magnus.models.fields.FlexibleForeignKey')(related_name='+', db_column='efid', to=orm['magnus.EFUser'])),
            ('visitor_agent', self.gf('magnus.models.fields.FlexibleForeignKey')(related_name='+', to=orm['magnus.VisitorAgent'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['EFUserVisitorAgent'])

        # Adding unique constraint on 'EFUserVisitorAgent', fields ['ef_user', 'visitor_agent']
        db.create_unique('ef_users_visitor_agents', ['efid', 'visitor_agent_id'])

    def backwards(self, orm):
        # Removing unique constraint on 'EFUserVisitorAgent', fields ['ef_user', 'visitor_agent']
        db.delete_unique('ef_users_visitor_agents', ['efid', 'visitor_agent_id'])

        # Removing unique constraint on 'Visit', fields ['session_id', 'fb_app']
        db.delete_unique('visits', ['session_id', 'fb_app_id'])

        # Removing unique constraint on 'ClientFBAppUser', fields ['client', 'fb_app_user']
        db.delete_unique('clients_fb_app_users', ['client_id', 'fb_app_user_id'])

        # Removing unique constraint on 'FBUserToken', fields ['api', 'fb_app_user']
        db.delete_unique('fb_user_tokens', ['api', 'fb_app_user_id'])

        # Removing unique constraint on 'FBAppUser', fields ['ef_user', 'fb_app']
        db.delete_unique('fb_app_users', ['efid', 'fb_app_id'])

        # Removing unique constraint on 'FBAppUser', fields ['fbid', 'fb_app']
        db.delete_unique('fb_app_users', ['fbid', 'fb_app_id'])

        # Deleting model 'FBApp'
        db.delete_table('fb_apps')

        # Removing M2M table for field current_permissions on 'FBApp'
        db.delete_table('fb_apps_fb_permissions')

        # Deleting model 'FBPermission'
        db.delete_table('fb_permissions')

        # Deleting model 'FBAppUser'
        db.delete_table('fb_app_users')

        # Deleting model 'EFUser'
        db.delete_table('ef_users')

        # Deleting model 'FBUserToken'
        db.delete_table('fb_user_tokens')

        # Deleting model 'Campaign'
        db.delete_table('campaigns')

        # Deleting model 'Client'
        db.delete_table('clients')

        # Deleting model 'ClientFBAppUser'
        db.delete_table('clients_fb_app_users')

        # Deleting model 'Event'
        db.delete_table('events')

        # Deleting model 'Visit'
        db.delete_table('visits')

        # Deleting model 'VisitorAgent'
        db.delete_table('visitor_agents')

        # Deleting model 'EFUserVisitorAgent'
        db.delete_table('ef_users_visitor_agents')

    models = {
        u'magnus.campaign': {
            'Meta': {'object_name': 'Campaign', 'db_table': "'campaigns'"},
            'campaign_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'campaigns'", 'to': u"orm['magnus.Client']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.client': {
            'Meta': {'object_name': 'Client', 'db_table': "'clients'"},
            'client_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'codename': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fb_app_users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'connected_clients'", 'blank': 'True', 'through': u"orm['magnus.ClientFBAppUser']", 'to': u"orm['magnus.FBAppUser']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.clientfbappuser': {
            'Meta': {'unique_together': "(('client', 'fb_app_user'),)", 'object_name': 'ClientFBAppUser', 'db_table': "'clients_fb_app_users'"},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['magnus.Client']"}),
            'client_app_user_id': ('magnus.models.fields.BigSerialField', [], {'primary_key': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fb_app_user': ('magnus.models.fields.FlexibleForeignKey', [], {'related_name': "'+'", 'to': u"orm['magnus.FBAppUser']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.efuser': {
            'Meta': {'object_name': 'EFUser', 'db_table': "'ef_users'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'efid': ('magnus.models.fields.BigSerialField', [], {'primary_key': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.efuservisitoragent': {
            'Meta': {'unique_together': "(('ef_user', 'visitor_agent'),)", 'object_name': 'EFUserVisitorAgent', 'db_table': "'ef_users_visitor_agents'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ef_user': ('magnus.models.fields.FlexibleForeignKey', [], {'related_name': "'+'", 'db_column': "'efid'", 'to': u"orm['magnus.EFUser']"}),
            'ef_user_visitor_agent_id': ('magnus.models.fields.BigSerialField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'visitor_agent': ('magnus.models.fields.FlexibleForeignKey', [], {'related_name': "'+'", 'to': u"orm['magnus.VisitorAgent']"})
        },
        u'magnus.event': {
            'Meta': {'ordering': "('event_datetime',)", 'object_name': 'Event', 'db_table': "'events'"},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'null': 'True', 'to': u"orm['magnus.Campaign']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('magnus.models.fields.JSONField', [], {}),
            'event_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'event_id': ('magnus.models.fields.BigSerialField', [], {'primary_key': 'True'}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'visit': ('magnus.models.fields.FlexibleForeignKey', [], {'related_name': "'events'", 'to': u"orm['magnus.Visit']"})
        },
        u'magnus.fbapp': {
            'Meta': {'ordering': "('namespace',)", 'object_name': 'FBApp', 'db_table': "'fb_apps'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_api': ('django.db.models.fields.DecimalField', [], {'default': "'2.2'", 'max_digits': '3', 'decimal_places': '1'}),
            'current_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'current_apps'", 'blank': 'True', 'db_table': "'fb_apps_fb_permissions'", 'to': u"orm['magnus.FBPermission']"}),
            'fb_app_id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'namespace': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.fbappuser': {
            'Meta': {'unique_together': "(('fbid', 'fb_app'), ('ef_user', 'fb_app'))", 'object_name': 'FBAppUser', 'db_table': "'fb_app_users'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ef_user': ('magnus.models.fields.FlexibleForeignKey', [], {'related_name': "'fb_app_users'", 'db_column': "'efid'", 'to': u"orm['magnus.EFUser']"}),
            'fb_app': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fb_app_users'", 'to': u"orm['magnus.FBApp']"}),
            'fb_app_user_id': ('magnus.models.fields.BigSerialField', [], {'primary_key': 'True'}),
            'fbid': ('django.db.models.fields.BigIntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.fbpermission': {
            'Meta': {'ordering': "('code',)", 'object_name': 'FBPermission', 'db_table': "'fb_permissions'"},
            'code': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'primary_key': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.fbusertoken': {
            'Meta': {'unique_together': "(('api', 'fb_app_user'),)", 'object_name': 'FBUserToken', 'db_table': "'fb_user_tokens'"},
            'access_token': ('django.db.models.fields.TextField', [], {}),
            'api': ('django.db.models.fields.DecimalField', [], {'default': "'2.2'", 'max_digits': '3', 'decimal_places': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expiration': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'fb_app_user': ('magnus.models.fields.FlexibleForeignKey', [], {'related_name': "'fb_user_tokens'", 'to': u"orm['magnus.FBAppUser']"}),
            'fb_user_token_id': ('magnus.models.fields.BigSerialField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.visit': {
            'Meta': {'unique_together': "(('session_id', 'fb_app'),)", 'object_name': 'Visit', 'db_table': "'visits'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fb_app': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'visits'", 'null': 'True', 'to': u"orm['magnus.FBApp']"}),
            'fbid': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'referer': ('django.db.models.fields.CharField', [], {'max_length': '1028', 'blank': 'True'}),
            'session_id': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'source': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'visit_id': ('magnus.models.fields.BigSerialField', [], {'primary_key': 'True'}),
            'visitor_agent': ('magnus.models.fields.FlexibleForeignKey', [], {'related_name': "'visits'", 'to': u"orm['magnus.VisitorAgent']"})
        },
        u'magnus.visitoragent': {
            'Meta': {'object_name': 'VisitorAgent', 'db_table': "'visitor_agents'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ef_users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'visitor_agents'", 'blank': 'True', 'through': u"orm['magnus.EFUserVisitorAgent']", 'to': u"orm['magnus.EFUser']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '1028', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40', 'blank': 'True'}),
            'visitor_agent_id': ('magnus.models.fields.BigSerialField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['magnus']
