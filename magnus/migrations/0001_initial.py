# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FBApp'
        db.create_table('fb_apps', (
            ('appid', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('current_api', self.gf('django.db.models.fields.DecimalField')(default='2.2', max_digits=3, decimal_places=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['FBApp'])

        # Adding model 'FBAppPermission'
        db.create_table('fb_app_permissions', (
            ('fb_app_permission_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magnus.FBApp'])),
            ('permission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magnus.FBPermission'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['FBAppPermission'])

        # Adding unique constraint on 'FBAppPermission', fields ['app', 'permission']
        db.create_unique('fb_app_permissions', ['app_id', 'permission_id'])

        # Adding model 'FBPermission'
        db.create_table('fb_permissions', (
            ('code', self.gf('django.db.models.fields.SlugField')(max_length=64, primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['FBPermission'])

        # Adding model 'FBAppUser'
        db.create_table('fb_app_users', (
            ('app_user_id', self.gf('magnus.models.BigSerialField')(primary_key=True)),
            ('fb_app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magnus.FBApp'])),
            ('fbid', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('ef_user', self.gf('magnus.models.FlexibleForeignKey')(to=orm['magnus.EFUser'], db_column='efid')),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['FBAppUser'])

        # Adding model 'EFUser'
        db.create_table('ef_users', (
            ('efid', self.gf('magnus.models.BigSerialField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['EFUser'])

        # Adding model 'FBUserToken'
        db.create_table('fb_user_tokens', (
            ('user_token_id', self.gf('magnus.models.BigSerialField')(primary_key=True)),
            ('app_user', self.gf('magnus.models.FlexibleForeignKey')(to=orm['magnus.FBAppUser'])),
            ('access_token', self.gf('django.db.models.fields.TextField')()),
            ('expiration', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('api', self.gf('django.db.models.fields.DecimalField')(default='2.2', max_digits=3, decimal_places=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['FBUserToken'])

        # Adding model 'Campaign'
        db.create_table('campaigns', (
            ('campaign_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='campaigns', to=orm['magnus.Client'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
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

        # Adding model 'ClientAppUser'
        db.create_table('client_app_users', (
            ('client_app_user_id', self.gf('magnus.models.BigSerialField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magnus.Client'])),
            ('app_user', self.gf('magnus.models.FlexibleForeignKey')(to=orm['magnus.FBAppUser'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['ClientAppUser'])

        # Adding unique constraint on 'ClientAppUser', fields ['client', 'app_user']
        db.create_unique('client_app_users', ['client_id', 'app_user_id'])

        # Adding model 'Event'
        db.create_table('events', (
            ('event_id', self.gf('magnus.models.BigSerialField')(primary_key=True)),
            ('visit', self.gf('magnus.models.FlexibleForeignKey')(to=orm['magnus.Visit'])),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magnus.Campaign'])),
            ('event_datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('data', self.gf('magnus.models.JSONField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['Event'])

        # Adding model 'Visit'
        db.create_table('visits', (
            ('visit_id', self.gf('magnus.models.BigSerialField')(primary_key=True)),
            ('visitor', self.gf('magnus.models.FlexibleForeignKey')(related_name='visits', to=orm['magnus.Visitor'])),
            ('session_id', self.gf('django.db.models.fields.CharField')(max_length=40, db_index=True)),
            ('app_id', self.gf('django.db.models.fields.BigIntegerField')(db_column='appid')),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(default='', max_length=1028, blank=True)),
            ('referer', self.gf('django.db.models.fields.CharField')(default='', max_length=1028, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['Visit'])

        # Adding unique constraint on 'Visit', fields ['session_id', 'app_id']
        db.create_unique('visits', ['session_id', 'appid'])

        # Adding model 'Visitor'
        db.create_table('visitors', (
            ('visitor_id', self.gf('magnus.models.BigSerialField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('efid', self.gf('django.db.models.fields.BigIntegerField')(unique=True, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['Visitor'])


    def backwards(self, orm):
        # Deleting model 'FBApp'
        db.delete_table('fb_apps')

        # Deleting model 'FBAppPermission'
        db.delete_table('fb_app_permissions')

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

        # Deleting model 'ClientAppUser'
        db.delete_table('client_app_users')

        # Deleting model 'Event'
        db.delete_table('events')

        # Deleting model 'Visit'
        db.delete_table('visits')

        # Deleting model 'Visitor'
        db.delete_table('visitors')


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
            'app_users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['magnus.FBAppUser']", 'through': u"orm['magnus.ClientAppUser']", 'symmetrical': 'False'}),
            'client_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'codename': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.clientappuser': {
            'Meta': {'unique_together': "(('client', 'app_user'),)", 'object_name': 'ClientAppUser', 'db_table': "'client_app_users'"},
            'app_user': ('magnus.models.FlexibleForeignKey', [], {'to': u"orm['magnus.FBAppUser']"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['magnus.Client']"}),
            'client_app_user_id': ('magnus.models.BigSerialField', [], {'primary_key': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.efuser': {
            'Meta': {'object_name': 'EFUser', 'db_table': "'ef_users'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'efid': ('magnus.models.BigSerialField', [], {'primary_key': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.event': {
            'Meta': {'object_name': 'Event', 'db_table': "'events'"},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['magnus.Campaign']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('magnus.models.JSONField', [], {}),
            'event_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'event_id': ('magnus.models.BigSerialField', [], {'primary_key': 'True'}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'visit': ('magnus.models.FlexibleForeignKey', [], {'to': u"orm['magnus.Visit']"})
        },
        u'magnus.fbapp': {
            'Meta': {'ordering': "('name',)", 'object_name': 'FBApp', 'db_table': "'fb_apps'"},
            'appid': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_api': ('django.db.models.fields.DecimalField', [], {'default': "'2.2'", 'max_digits': '3', 'decimal_places': '1'}),
            'current_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['magnus.FBPermission']", 'symmetrical': 'False', 'through': u"orm['magnus.FBAppPermission']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.fbapppermission': {
            'Meta': {'unique_together': "(('app', 'permission'),)", 'object_name': 'FBAppPermission', 'db_table': "'fb_app_permissions'"},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['magnus.FBApp']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fb_app_permission_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['magnus.FBPermission']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.fbappuser': {
            'Meta': {'object_name': 'FBAppUser', 'db_table': "'fb_app_users'"},
            'app_user_id': ('magnus.models.BigSerialField', [], {'primary_key': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ef_user': ('magnus.models.FlexibleForeignKey', [], {'to': u"orm['magnus.EFUser']", 'db_column': "'efid'"}),
            'fb_app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['magnus.FBApp']"}),
            'fbid': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.fbpermission': {
            'Meta': {'ordering': "('code',)", 'object_name': 'FBPermission', 'db_table': "'fb_permissions'"},
            'code': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'primary_key': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.fbusertoken': {
            'Meta': {'object_name': 'FBUserToken', 'db_table': "'fb_user_tokens'"},
            'access_token': ('django.db.models.fields.TextField', [], {}),
            'api': ('django.db.models.fields.DecimalField', [], {'default': "'2.2'", 'max_digits': '3', 'decimal_places': '1'}),
            'app_user': ('magnus.models.FlexibleForeignKey', [], {'to': u"orm['magnus.FBAppUser']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expiration': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_token_id': ('magnus.models.BigSerialField', [], {'primary_key': 'True'})
        },
        u'magnus.visit': {
            'Meta': {'unique_together': "(('session_id', 'app_id'),)", 'object_name': 'Visit', 'db_table': "'visits'"},
            'app_id': ('django.db.models.fields.BigIntegerField', [], {'db_column': "'appid'"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'referer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1028', 'blank': 'True'}),
            'session_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1028', 'blank': 'True'}),
            'visit_id': ('magnus.models.BigSerialField', [], {'primary_key': 'True'}),
            'visitor': ('magnus.models.FlexibleForeignKey', [], {'related_name': "'visits'", 'to': u"orm['magnus.Visitor']"})
        },
        u'magnus.visitor': {
            'Meta': {'object_name': 'Visitor', 'db_table': "'visitors'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'efid': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'visitor_id': ('magnus.models.BigSerialField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['magnus']
