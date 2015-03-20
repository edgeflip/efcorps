# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Campaign'
        db.delete_table('campaigns')

        # Adding model 'ContentVehicle'
        db.create_table('content_vehicles', (
            ('content_vehicle_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('urn', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('content_vehicle_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_vehicles', to=orm['magnus.ContentVehicleType'])),
            ('intermediate_vehicle', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='linking_vehicles', null=True, to=orm['magnus.ContentVehicle'])),
            ('client_content', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_vehicles', to=orm['magnus.ClientContent'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['ContentVehicle'])

        # Adding unique constraint on 'ContentVehicle', fields ['urn', 'content_vehicle_type']
        db.create_unique('content_vehicles', ['urn', 'content_vehicle_type_id'])

        # Adding model 'ContentVehicleType'
        db.create_table('content_vehicle_types', (
            ('codename', self.gf('django.db.models.fields.SlugField')(max_length=50, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['ContentVehicleType'])

        # Adding model 'ClientContent'
        db.create_table('client_content', (
            ('client_content_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='client_content', to=orm['magnus.Client'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=2048)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['ClientContent'])

        # Adding unique constraint on 'ClientContent', fields ['name', 'client']
        db.create_unique('client_content', ['name', 'client_id'])

        # Adding unique constraint on 'ClientContent', fields ['url', 'client']
        db.create_unique('client_content', ['url', 'client_id'])

        # Deleting field 'Event.campaign'
        db.delete_column('events', 'campaign_id')

        # Adding field 'Event.content_vehicle'
        db.add_column('events', 'content_vehicle',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', null=True, to=orm['magnus.ContentVehicle']),
                      keep_default=False)

    def backwards(self, orm):
        # Removing unique constraint on 'ClientContent', fields ['url', 'client']
        db.delete_unique('client_content', ['url', 'client_id'])

        # Removing unique constraint on 'ClientContent', fields ['name', 'client']
        db.delete_unique('client_content', ['name', 'client_id'])

        # Removing unique constraint on 'ContentVehicle', fields ['urn', 'content_vehicle_type']
        db.delete_unique('content_vehicles', ['urn', 'content_vehicle_type_id'])

        # Adding model 'Campaign'
        db.create_table('campaigns', (
            ('campaign_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='campaigns', to=orm['magnus.Client'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'magnus', ['Campaign'])

        # Deleting model 'ContentVehicle'
        db.delete_table('content_vehicles')

        # Deleting model 'ContentVehicleType'
        db.delete_table('content_vehicle_types')

        # Deleting model 'ClientContent'
        db.delete_table('client_content')

        # Adding field 'Event.campaign'
        db.add_column('events', 'campaign',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', null=True, to=orm['magnus.Campaign']),
                      keep_default=False)

        # Deleting field 'Event.content_vehicle'
        db.delete_column('events', 'content_vehicle_id')

    models = {
        u'magnus.client': {
            'Meta': {'object_name': 'Client', 'db_table': "'clients'"},
            'client_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'codename': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fb_app_users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'connected_clients'", 'blank': 'True', 'through': u"orm['magnus.ClientFBAppUser']", 'to': u"orm['magnus.FBAppUser']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.clientcontent': {
            'Meta': {'unique_together': "(('name', 'client'), ('url', 'client'))", 'object_name': 'ClientContent', 'db_table': "'client_content'"},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'client_content'", 'to': u"orm['magnus.Client']"}),
            'client_content_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2048'})
        },
        u'magnus.clientfbappuser': {
            'Meta': {'unique_together': "(('client', 'fb_app_user'),)", 'object_name': 'ClientFBAppUser', 'db_table': "'clients_fb_app_users'"},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['magnus.Client']"}),
            'client_app_user_id': ('magnus.models.fields.BigSerialField', [], {'primary_key': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fb_app_user': ('magnus.models.fields.FlexibleForeignKey', [], {'related_name': "'+'", 'to': u"orm['magnus.FBAppUser']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.contentvehicle': {
            'Meta': {'unique_together': "(('urn', 'content_vehicle_type'),)", 'object_name': 'ContentVehicle', 'db_table': "'content_vehicles'"},
            'client_content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_vehicles'", 'to': u"orm['magnus.ClientContent']"}),
            'content_vehicle_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'content_vehicle_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_vehicles'", 'to': u"orm['magnus.ContentVehicleType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'intermediate_vehicle': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'linking_vehicles'", 'null': 'True', 'to': u"orm['magnus.ContentVehicle']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'urn': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'magnus.contentvehicletype': {
            'Meta': {'ordering': "('codename',)", 'object_name': 'ContentVehicleType', 'db_table': "'content_vehicle_types'"},
            'codename': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'magnus.efapikey': {
            'Meta': {'object_name': 'EFApiKey', 'db_table': "'ef_api_keys'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ef_api_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'efapikeys'", 'db_column': "'ef_api_user_name'", 'to': u"orm['magnus.EFApiUser']"}),
            'ef_app': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'efapikeys'", 'db_column': "'ef_app_name'", 'to': u"orm['magnus.EFApp']"}),
            'key': ('django.db.models.fields.SlugField', [], {'default': "'7894eb6b702cede7ff8d9872bfc71b9c6260e7d5'", 'max_length': '40', 'primary_key': 'True', 'db_column': "'ef_api_key'"}),
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
            'content_vehicle': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'null': 'True', 'to': u"orm['magnus.ContentVehicle']"}),
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
