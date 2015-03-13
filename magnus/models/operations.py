from magnus import models


def get_or_create_efid(fb_app_id, fbid, email, name):
    """Return a new or existing user identifier (`efid`) for a user as given.

    All arguments are required, though `email` and `name` may be empty entities.

    """
    try:
        return models.EFUser.objects.values_list('efid', flat=True).get(
            fb_app_user__fb_app_id=fb_app_id,
            fb_app_user__fbid=fbid,
        )
    except models.EFUser.DoesNotExist:
        pass

    if email:
        (ef_user, _created) = models.EFUser.objects.get_or_create(email=email,
                                                                  defaults={'name': name})
    else:
        ef_user = models.EFUser.objects.create(name=name)

    ef_user.fb_app_users.get_or_create(fb_app_id=fb_app_id, fbid=fbid)
    return ef_user.efid
