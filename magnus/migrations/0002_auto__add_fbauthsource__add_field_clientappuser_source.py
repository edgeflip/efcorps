# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FBAuthSource'
        db.create_table('fb_auth_sources', (
            ('source_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('pretty_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['FBAuthSource'])

        # Adding field 'ClientAppUser.source'
        db.add_column('client_app_users', 'source',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magnus.FBAuthSource'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'FBAuthSource'
        db.delete_table('fb_auth_sources')

        # Deleting field 'ClientAppUser.source'
        db.delete_column('client_app_users', 'source_id')


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
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['magnus.FBAuthSource']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.efuser': {
            'Meta': {'object_name': 'EFUser', 'db_table': "'ef_users'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'efid': ('magnus.models.BigSerialField', [], {'primary_key': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_index': 'True'}),
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
            'Meta': {'unique_together': "(('fb_app', 'fbid'),)", 'object_name': 'FBAppUser', 'db_table': "'fb_app_users'"},
            'app_user_id': ('magnus.models.BigSerialField', [], {'primary_key': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ef_user': ('magnus.models.FlexibleForeignKey', [], {'related_name': "'app_users'", 'db_column': "'efid'", 'to': u"orm['magnus.EFUser']"}),
            'fb_app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['magnus.FBApp']"}),
            'fbid': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.fbauthsource': {
            'Meta': {'object_name': 'FBAuthSource', 'db_table': "'fb_auth_sources'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'pretty_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'source_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
