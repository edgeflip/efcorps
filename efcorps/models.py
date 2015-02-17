from decimal import Decimal
from django.utils.crypto import get_random_string
import string

from jsonfield import JSONField

from django.db import models


class FBApp(models.Model):
    appid = models.BigIntegerField('FB App ID', primary_key=True)
    name = models.CharField('FB App Namespace', max_length=255, unique=True)
    secret = models.CharField('FB App Secret', max_length=32)
    api = models.DecimalField('FB API Version', max_digits=3, decimal_places=1,
                              default=Decimal('2.2'))
    permissions = models.ManyToManyField('FBPermission', blank=True)

    class Meta(object):
        db_table = 'fb_apps'
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class FBPermission(models.Model):

    code = models.SlugField(max_length=64, primary_key=True)

    class Meta(object):
        db_table = 'fb_permissions'
        ordering = ('code',)

    def __unicode__(self):
        return self.code


class FBAppUser(models.Model):
    app = models.ForeignKey('FBApp')
    asid = models.BigIntegerField('App-scoped ID')
    person = models.ForeignKey('Person')

    class Meta(object):
        db_table = 'fb_app_users'


class Person(models.Model):
    name = models.CharField('Person Name')

    class Meta(object):
        db_table = 'persons'


class FBUserToken(models.Model):
    app_user = models.ForeignKey('FBAppUser')
    access_token = models.CharField('Access Token')
    expiration = models.DateTimeField()

    class Meta(object):
        db_table = 'fb_user_tokens'


class Campaign(models.Model):
    client = models.ForeignKey('Client')
    name = models.CharField('Campaign Name')

    class Meta(object):
        db_table = 'campaigns'


class Client(models.Model):
    name = models.CharField('Client Name')

    class Meta(object):
        db_table = 'clients'


class ClientAppUser(models.Model):
    client = models.ForeignKey('Client')
    app_user = models.ForeignKey('FBAppUser')

    class Meta(object):
        db_table = 'client_app_users'


class Event(models.Model):
    visit = models.ForeignKey('Visit')
    event_type = models.CharField('Event Type')
    campaign = models.ForeignKey('Campaign')
    event_datetime = models.DateTimeField()
    data = JSONField()


class Visit(models.Model):
    visit_id = models.AutoField(primary_key=True)
    visitor = models.ForeignKey('Visitor', related_name='visits')
    session_id = models.CharField(db_index=True, max_length=40)
    app_id = models.BigIntegerField(db_column='appid')
    ip = models.GenericIPAddressField()
    user_agent = models.CharField(blank=True, default='', max_length=1028)
    referer = models.CharField(blank=True, default='', max_length=1028)
    source = models.CharField(blank=True, default='', db_index=True, max_length=256)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        db_table = 'visits'
        get_latest_by = 'created'
        unique_together = ('session_id', 'app_id')

    def __unicode__(self):
        return u"{} [{}]".format(self.session_id, self.app_id)


class Visitor(models.Model):

    visitor_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=40)
    fbid = models.BigIntegerField(unique=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        db_table = 'visitors'

    @classmethod
    def get_new_uuid(cls):
        """Return a UUID that isn't being used."""
        while True:
            uuid = get_random_string(40, string.ascii_uppercase + string.digits)
            if not cls._default_manager.filter(uuid=uuid).exists():
                return uuid

    def save(self, *args, **kws):
        # Ensure uuid is set:
        if not self.uuid:
            self.uuid = self.get_new_uuid()
        return super(Visitor, self).save(*args, **kws)

    def __unicode__(self):
        return u"{} [{}]".format(self.uuid, self.fbid or '')
