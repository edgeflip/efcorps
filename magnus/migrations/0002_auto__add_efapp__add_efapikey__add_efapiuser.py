# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EFApp'
        db.create_table('ef_apps', (
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=30, primary_key=True, db_column='ef_app_name')),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['EFApp'])

        # Adding model 'EFApiKey'
        db.create_table('ef_api_keys', (
            ('key', self.gf('django.db.models.fields.SlugField')(default='ab57e82bd8d05f4b45b03425ac4b0681965758c0', max_length=40, primary_key=True, db_column='ef_api_key')),
            ('ef_api_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='efapikeys', db_column='ef_api_user_name', to=orm['magnus.EFApiUser'])),
            ('ef_app', self.gf('django.db.models.fields.related.ForeignKey')(related_name='efapikeys', db_column='ef_app_name', to=orm['magnus.EFApp'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['EFApiKey'])

        # Adding model 'EFApiUser'
        db.create_table('ef_api_users', (
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=30, primary_key=True, db_column='ef_api_user_name')),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['EFApiUser'])

    def backwards(self, orm):
        # Deleting model 'EFApp'
        db.delete_table('ef_apps')

        # Deleting model 'EFApiKey'
        db.delete_table('ef_api_keys')

        # Deleting model 'EFApiUser'
        db.delete_table('ef_api_users')

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
        u'magnus.efapikey': {
            'Meta': {'object_name': 'EFApiKey', 'db_table': "'ef_api_keys'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ef_api_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'efapikeys'", 'db_column': "'ef_api_user_name'", 'to': u"orm['magnus.EFApiUser']"}),
            'ef_app': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'efapikeys'", 'db_column': "'ef_app_name'", 'to': u"orm['magnus.EFApp']"}),
            'key': ('django.db.models.fields.SlugField', [], {'default': "'59d8388c984eba42de2a86d6e7dcc8968b002db5'", 'max_length': '40', 'primary_key': 'True', 'db_column': "'ef_api_key'"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.efapiuser': {
            'Meta': {'object_name': 'EFApiUser', 'db_table': "'ef_api_users'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '30', 'primary_key': 'True', 'db_column': "'ef_api_user_name'"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.efapp': {
            'Meta': {'object_name': 'EFApp', 'db_table': "'ef_apps'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '30', 'primary_key': 'True', 'db_column': "'ef_app_name'"}),
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
