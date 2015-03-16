import hashlib
import hmac
import string
import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from . import base, fields, manager


DATABASE_ENCODING = getattr(settings, 'MAGNUS_DATABASE_ENCODING', 'utf-8')

DEFAULT_FB_API = Decimal('2.2')


class FBApp(base.BaseModel):
    """A Facebook "app"."""

    fb_app_id = models.BigIntegerField('FB App ID', primary_key=True)
    namespace = models.SlugField('FB App Namespace', max_length=255, unique=True)
    secret = models.CharField('FB App Secret', max_length=32)
    current_api = models.DecimalField('FB API Version',
                                      max_digits=3,
                                      decimal_places=1,
                                      default=DEFAULT_FB_API)
    current_permissions = models.ManyToManyField('magnus.FBPermission',
                                                 db_table='fb_apps_fb_permissions',
                                                 related_name='current_apps',
                                                 blank=True)

    # NOTE: The implicitly-defined "through" model whose table records the
    # many-to-many relationship between FBApp and FBPermission --
    # fb_apps_fb_permissions -- is still available, (in the unlikely chance it's
    # helpful or needed), at:
    #     models.FBApp.current_permissions.through
    # However, in letting Django manage it, all necessary operations should be
    # covered by the FBApp.current_permissions descriptor (and the
    # FBPermission.current_apps manager).

    class Meta(base.BaseModel.Meta):
        db_table = 'fb_apps'
        ordering = ('namespace',)

    def __unicode__(self):
        return self.namespace


class FBPermission(base.BaseModel):
    """A Facebook API permission, granted by a Facebook user."""

    code = models.SlugField(max_length=64, primary_key=True)

    objects = manager.TypeObjectManager()

    class Codes(objects.Types):

        PUBLIC_PROFILE = 'public_profile'
        USER_FRIENDS = 'user_friends'
        EMAIL = 'email'
        USER_ACTIVITIES = 'user_activities'
        USER_BIRTHDAY = 'user_birthday'
        USER_LOCATION = 'user_location'
        USER_INTERESTS = 'user_interests'
        USER_LIKES = 'user_likes'
        USER_PHOTOS = 'user_photos'
        USER_RELATIONSHIPS = 'user_relationships'
        USER_STATUS = 'user_status'
        USER_VIDEOS = 'user_videos'

        def __str__(self):
            return self.value

    class Meta(base.BaseModel.Meta):
        db_table = 'fb_permissions'
        ordering = ('code',)

    def __unicode__(self):
        return self.code


class FBAppUser(base.BaseModel):
    """A user of Facebook, as identified through a particular Facebook app."""

    related_name = 'fb_app_users'
    related_query_name = 'fb_app_user'

    fb_app_user_id = fields.BigSerialField(primary_key=True)
    fbid = models.BigIntegerField('App-scoped Facebook ID') # indexed below
    fb_app = models.ForeignKey('magnus.FBApp', related_name=related_name)
    ef_user = fields.FlexibleForeignKey('magnus.EFUser',
                                        db_column='efid',
                                        related_name=related_name,
                                        related_query_name=related_query_name)

    class Meta(base.BaseModel.Meta):
        db_table = 'fb_app_users'
        unique_together = (('fbid', 'fb_app'), ('ef_user', 'fb_app'))

    def __unicode__(self):
        return u'{} [{}]'.format(self.fbid, self.fb_app_id)


class EFUser(base.BaseModel):
    """A uniquely identified end-user."""

    efid = fields.BigSerialField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField('E-mail Address', max_length=254, unique=True, null=True, blank=True)

    class Meta(base.BaseModel.Meta):
        db_table = 'ef_users'

    def __unicode__(self):
        return u'{}: {} [{}]'.format(self.efid, self.name, self.email)

    def __repr__(self):
        return u"<{}: {} {} [{}]".format(self.__class__.__name__, self.efid, self.name, self.email)


class FBUserToken(base.BaseModel):
    """A Facebook authentication token authorizing access to a user's data."""

    fb_user_token_id = fields.BigSerialField(primary_key=True)
    fb_app_user = fields.FlexibleForeignKey('magnus.FBAppUser', related_name='fb_user_tokens')
    access_token = models.TextField('Access Token')
    expiration = models.DateTimeField(db_index=True)
    api = models.DecimalField('FB API Version', max_digits=3, decimal_places=1,
                              default=DEFAULT_FB_API) # indexed below

    # DEFERRED: we could record the permissions granted through the token (via
    # another many-to-many with FBPermission).

    class Meta(base.BaseModel.Meta):
        db_table = 'fb_user_tokens'
        get_latest_by = 'expiration'
        unique_together = ('api', 'fb_app_user')

    def __unicode__(self):
        return self.access_token

    def __repr__(self):
        return '<{}: {} [{}]>'.format(self.__class__.__name__, self.fb_app_user_id, self.api)


class Campaign(base.BaseModel):

    campaign_id = models.AutoField(primary_key=True)
    name = models.CharField('Campaign Name', max_length=255)
    client = models.ForeignKey('magnus.Client', related_name='campaigns')

    class Meta(base.BaseModel.Meta):
        db_table = 'campaigns'

    def __unicode__(self):
        return self.name


class Client(base.BaseModel):
    """A business client, for whom we engage FBAppUsers, through Campaigns."""

    client_id = models.AutoField(primary_key=True)
    name = models.CharField('Client Name', max_length=255)
    codename = models.SlugField(unique=True, blank=True, editable=False)
    fb_app_users = models.ManyToManyField('magnus.FBAppUser',
                                          through='magnus.ClientFBAppUser',
                                          related_name='connected_clients',
                                          blank=True)

    # NOTE: Because the many-to-many relationship between Client and FBAppUser
    # is explicitly defined, through ClientFBAppUser, the Client.fb_app_users
    # manager is available for querying FBAppUsers, but does not support
    # addition of FBAppUsers to a Client; rather, you must create (and delete)
    # ClientFBAppUsers.

    class Meta(base.BaseModel.Meta):
        db_table = 'clients'

    def set_codename(self):
        if not self.name:
            raise ValueError("Cannot generate codename from empty name")
        name = self.name if isinstance(self.name, unicode) else self.name.decode(DATABASE_ENCODING)
        self.codename = slugify(name)

    def save(self, *args, **kws):
        if not self.codename:
            self.set_codename()
        return super(Client, self).save(*args, **kws)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.codename)


class ClientFBAppUser(base.BaseModel):
    """Explicit intermediary recording the many-to-many relationship between
    FBAppUsers and the Clients with whose campaigns they've engaged.

    Note that, by "engaged", the intent is to exclude users who may *click* but
    refuse to "connect" (i.e. authorization). However, this may *include* users
    who click a client's campaign link and connect *automatically*, (because
    they've already authorized the Facebook app before, with another client).

    """
    client_app_user_id = fields.BigSerialField(primary_key=True)
    client = models.ForeignKey('magnus.Client', related_name='+')
    fb_app_user = fields.FlexibleForeignKey('magnus.FBAppUser', related_name='+')
    # NOTE: Reverse managers are useful, but here suppressed ('+'), to avoid
    # confusion with the direct Client <=> FBAppUser relationship.

    class Meta(base.BaseModel.Meta):
        db_table = 'clients_fb_app_users'
        unique_together = ('client', 'fb_app_user')


class Event(base.BaseModel):
    """The atomic record of an end-user's interaction with one of our apps,
    and of any notable occurrence affecting a specific end-user's experience.

    This model purposefully limits its fields to the common minimum, necessary
    for processing and simple querying, and provides a JSON-storing field,
    `data`, for the storage of any event-specific details.

    """
    event_id = fields.BigSerialField(primary_key=True)
    visit = fields.FlexibleForeignKey('magnus.Visit', related_name='events')
    event_type = models.CharField('Event Type', max_length=64)
    campaign = models.ForeignKey('magnus.Campaign', null=True, related_name='events')
    event_datetime = models.DateTimeField(db_index=True, default=timezone.now)
    data = fields.JSONField()

    class Meta(base.BaseModel.Meta):
        db_table = 'events'
        ordering = ('event_datetime',)


class Visit(base.BaseModel):
    """An end-user's session of interaction with one of our apps.

    A visit may or may not be capable of recording the Facebook App or,
    separately, the Facebook user ID. Property `fb_app_user` is provided to
    dynamically look up the visit's FBAppUser, if this data was recorded.

    Note, however, that having identified the FBAppUser, the visit's
    VisitorAgent should *also* be linked to an EFUser, and the visit should
    thereby *also* link to the correct FBAppUser by following that path:

        visit => visitor_agent => ef_user(s) => fb_app_user(s)

    However, the link is additionally provided from Visit, so as to easily
    record partial data, (e.g., the app is known but the Facebook user ID is
    not), so as to more easily query the relationship, and so as to
    disambiguate the relationship when a visit's visitor_agent is shared
    between users.

    """
    related_name = 'visits'

    visit_id = fields.BigSerialField(primary_key=True)
    visitor_agent = fields.FlexibleForeignKey('magnus.VisitorAgent', related_name=related_name)
    session_id = models.CharField(max_length=40) # indexed below
    ip = models.GenericIPAddressField()
    fb_app = models.ForeignKey('magnus.FBApp', null=True, related_name=related_name)
    fbid = models.BigIntegerField('App-scoped Facebook ID', null=True)
    referer = models.CharField(blank=True, max_length=1028)
    source = models.SlugField(blank=True)

    class Meta(base.BaseModel.Meta):
        db_table = 'visits'
        get_latest_by = 'created'
        unique_together = ('session_id', 'fb_app')

    @property
    def fb_app_user(self):
        return self.fb_app and self.fbid and self.fb_app.fb_app_users.get(fbid=self.fbid)

    def __unicode__(self):
        return u"{} [{}]".format(self.session_id, self.fb_app_id)


class VisitorAgent(base.BaseModel):
    """A uniquely-identified "user agent", or visiting device, through which an
    EFUser performs Visits.

    The `uuid` is intended to be stored in the user agent (in a cookie), for
    reidentification of visitors in subsequent visits.

    """
    visitor_agent_id = fields.BigSerialField(primary_key=True)
    uuid = models.CharField(blank=True, unique=True, max_length=40)
    ef_users = models.ManyToManyField('magnus.EFUser',
                                      through='magnus.EFUserVisitorAgent',
                                      related_name='visitor_agents',
                                      blank=True)
    user_agent = models.CharField(blank=True, max_length=1028)

    # NOTE: Because the many-to-many relationship between VisitorAgent and
    # EFUser is explicitly defined, through EFUserVisitorAgent, the
    # VisitorAgent.ef_users manager is available for querying EFUsers, but does
    # not support addition of VisitorAgents to an EFUser; rather, you must
    # create (and delete) EFUserVisitorAgents.

    class Meta(base.BaseModel.Meta):
        db_table = 'visitor_agents'

    @classmethod
    def get_new_uuid(cls):
        """Return a UUID that isn't being used."""
        while True:
            uuid = get_random_string(40, string.ascii_uppercase + string.digits)
            if not cls._default_manager.filter(uuid=uuid).exists():
                return uuid

    def set_uuid(self):
        self.uuid = self.get_new_uuid()

    def save(self, *args, **kws):
        # Ensure uuid is set:
        if not self.uuid:
            self.set_uuid()
        return super(VisitorAgent, self).save(*args, **kws)

    def __unicode__(self):
        return self.uuid

    def __repr__(self):
        efids = self.ef_users.values_list('efid', flat=True) or (None,)
        signature = " ".join("[{}]".format(efid) for efid in efids)
        return u"<{}: {} {}>".format(self.__class__.__name__, self.uuid, signature)


class EFUserVisitorAgent(base.BaseModel):
    """Explicit intermediary recording the many-to-many relationship between
    EFUser and VisitorAgent.

    When the relationship can be identified at all, it "should" -- that is, most
    of the time -- in fact be one-to-many, (or even one-to-one): each EFUser
    visits us using one or more of their own user agents. However, users *may*
    share devices, which we support here, without data imprecision or loss.

    """
    ef_user_visitor_agent_id = fields.BigSerialField(primary_key=True)
    ef_user = fields.FlexibleForeignKey('magnus.EFUser', db_column='efid', related_name='+')
    visitor_agent = fields.FlexibleForeignKey('magnus.VisitorAgent', related_name='+')

    class Meta(base.BaseModel.Meta):
        db_table = 'ef_users_visitor_agents'
        unique_together = ('ef_user', 'visitor_agent')


class EFApp(base.BaseModel):
    """An Edgeflip app (providing an API)."""

    name = models.SlugField(primary_key=True, max_length=30, db_column='ef_app_name')

    class Meta(base.BaseModel.Meta):
        db_table = 'ef_apps'


class EFApiUser(base.BaseModel):
    """A consumer of an Edgeflip app's API."""

    name = models.SlugField(primary_key=True, max_length=30, db_column='ef_api_user_name')

    class Meta(base.BaseModel.Meta):
        db_table = 'ef_api_users'


def generate_api_key():
    """Construct a new (ostensibly-unique) API key."""
    unique = uuid.uuid4()
    code = hmac.new(unique.bytes, digestmod=hashlib.sha1)
    return code.hexdigest()


class EFApiKey(base.BaseModel):
    """An Edgeflip API consumer's authentication key."""

    key = models.SlugField(primary_key=True,
                           default=generate_api_key,
                           max_length=40,
                           db_column='ef_api_key')

    ef_api_user = models.ForeignKey('magnus.EFApiUser',
                                    db_column='ef_api_user_name',
                                    related_name='efapikeys')

    ef_app = models.ForeignKey('magnus.EFApp',
                               db_column='ef_app_name',
                               related_name='efapikeys')

    generate_key = staticmethod(generate_api_key)

    class Meta(base.BaseModel.Meta):
        db_table = 'ef_api_keys'

# DEFERRED: ApiPermissions (off of EFApiUser or EFApiKey?)
