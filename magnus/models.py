from decimal import Decimal
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
import string
import json
from south.modelsinspector import add_introspection_rules

from django.db import models

add_introspection_rules([], ["^magnus\.models\.JSONField"])
add_introspection_rules([], ["^magnus\.models\.BigSerialField"])


class JSONField(models.Field):
    def db_type(self, connection):
        return 'json'

    def get_prep_value(self, value):
        return json.dumps(value)

    def to_python(self, value):
        if isinstance(value, basestring):
            try:
                return json.loads(value)
            except ValueError, exc:
                raise ValidationError(exc)

        try:
            self.get_prep_value(value)
        except ValueError, exc:
            raise ValidationError(exc)
        else:
            return value


class BigSerialField(models.AutoField):
    def db_type(self, connection):
        return 'bigserial'


class TimestampedModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True


class FBApp(TimestampedModel):
    appid = models.BigIntegerField('FB App ID', primary_key=True)
    name = models.CharField('FB App Namespace', max_length=255, unique=True)
    secret = models.CharField('FB App Secret', max_length=32)
    current_api = models.DecimalField('FB API Version', max_digits=3, decimal_places=1,
                              default=Decimal('2.2'))
    current_permissions = models.ManyToManyField('FBPermission', blank=True)

    class Meta(object):
        db_table = 'fb_apps'
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class FBPermission(TimestampedModel):

    code = models.SlugField(max_length=64, primary_key=True)

    class Meta(object):
        db_table = 'fb_permissions'
        ordering = ('code',)

    def __unicode__(self):
        return self.code


class FBAppUser(TimestampedModel):
    app_user_id = BigSerialField(primary_key=True)
    app = models.ForeignKey('FBApp')
    fbid = models.BigIntegerField('App-scoped Facebook ID', db_index=True)
    ef_user = models.ForeignKey('EFUser', db_column='efid')

    class Meta(object):
        db_table = 'fb_app_users'


class EFUser(TimestampedModel):
    efid = BigSerialField(primary_key=True)
    name = models.CharField('Person Name', max_length=255, db_index=True)

    class Meta(object):
        db_table = 'ef_users'


class FBUserToken(TimestampedModel):
    user_token_id = BigSerialField(primary_key=True)
    app_user = models.ForeignKey('FBAppUser')
    access_token = models.TextField('Access Token')
    expiration = models.DateTimeField(db_index=True)
    api = models.DecimalField('FB API Version', max_digits=3, decimal_places=1,
                              default=Decimal('2.2'))

    class Meta(object):
        db_table = 'fb_user_tokens'


class Campaign(TimestampedModel):
    campaign_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('Client', related_name='campaigns')
    name = models.CharField('Campaign Name', max_length=255)

    class Meta(object):
        db_table = 'campaigns'


class Client(TimestampedModel):
    client_id = models.AutoField(primary_key=True)
    name = models.CharField('Client Name', max_length=255)
    codename = models.SlugField(unique=True, blank=True, editable=False)
    app_users = models.ManyToManyField('FBAppUser', through='ClientAppUser')

    class Meta(object):
        db_table = 'clients'


class ClientAppUser(TimestampedModel):
    client_app_user_id = BigSerialField(primary_key=True)
    client = models.ForeignKey('Client')
    app_user = models.ForeignKey('FBAppUser')

    class Meta(object):
        db_table = 'client_app_users'
        unique_together = ('client', 'app_user')


class Event(TimestampedModel):
    event_id = BigSerialField(primary_key=True)
    visit = models.ForeignKey('Visit')
    event_type = models.CharField('Event Type', max_length=64)
    campaign = models.ForeignKey('Campaign')
    event_datetime = models.DateTimeField(db_index=True)
    data = JSONField()

    class Meta(object):
        db_table = 'events'


class Visit(TimestampedModel):
    visit_id = BigSerialField(primary_key=True)
    visitor = models.ForeignKey('Visitor', related_name='visits')
    session_id = models.CharField(db_index=True, max_length=40)
    app_id = models.BigIntegerField(db_column='appid')
    ip = models.GenericIPAddressField()
    user_agent = models.CharField(blank=True, default='', max_length=1028)
    referer = models.CharField(blank=True, default='', max_length=1028)

    class Meta(object):
        db_table = 'visits'
        get_latest_by = 'created'
        unique_together = ('session_id', 'app_id')

    def __unicode__(self):
        return u"{} [{}]".format(self.session_id, self.app_id)


class Visitor(TimestampedModel):

    visitor_id = BigSerialField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=40)
    efid = models.BigIntegerField(unique=True, null=True, blank=True)

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
        return u"{} [{}]".format(self.uuid, self.efid or '')
