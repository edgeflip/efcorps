import logging
import sys

from django.db import IntegrityError, transaction
from django.utils import six

from magnus import models


LOG = logging.getLogger(__name__)


def get_or_create_efid(fb_app_id, fbid, email, name):
    """Return a new or existing user identifier (`efid`) for a user as given.

    All arguments are required, though `email` and `name` may be empty entities.

    """
    # If we've logged this app-scoped fbid before it's just a look-up:
    try:
        return models.EFUser.objects.values_list('efid', flat=True).get(
            fb_app_user__fb_app_id=fb_app_id,
            fb_app_user__fbid=fbid,
        )
    except models.EFUser.DoesNotExist:
        pass

    # Nope, we'll have to create an FBAppUser, at the least.
    # The logic varies, just enough, depending on whether we have an email
    # (and therefore a uniqueness constraint).

    if email:
        # Use SELECT ... FOR UPDATE (in a transaction) so that we can safely
        # update the "name" of an existing EFUser.
        with transaction.atomic():
            (ef_user, _created) = (models.EFUser.objects.select_for_update()
                                   .get_or_create(email=email, defaults={'name': name}))
            if name:
                if not ef_user.name:
                    ef_user.name = name
                    ef_user.save(update_fields=['name'])
                elif name != ef_user.name:
                    LOG.warning("Name mismatch for user %s (%s)",
                                ef_user.efid, email, extra={'stack': True})

        ef_user.fb_app_users.get_or_create(fb_app_id=fb_app_id, fbid=fbid)
        return ef_user.efid

    # Without an email, there's not much we can do except avoid a race
    # condition.
    try:
        with transaction.atomic():
            ef_user = models.EFUser.objects.create(name=name)
            ef_user.fb_app_users.get_or_create(fb_app_id=fb_app_id, fbid=fbid)
            return ef_user.efid
    except IntegrityError:
        exc_info = sys.exc_info()
        # FBAppUser creation probably failed due to a race.
        # If that's so, we can simply retrieve the winner's efid.
        # (In the "email" branch, the competitors should share a single EFUser,
        # in which case `get_or_create()` does this for us.)
        try:
            return models.EFUser.objects.values_list('efid', flat=True).get(
                fb_app_user__fb_app_id=fb_app_id,
                fb_app_user__fbid=fbid,
            )
        except models.EFUser.DoesNotExist:
            # Nope, this is an issue we don't know how to handle.
            # Re-raise the exception with its original traceback.
            six.reraise(*exc_info)
