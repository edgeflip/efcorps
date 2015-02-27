from magnus.models import EFUser, FBAppUser
from django.db import IntegrityError


def get_or_create_efid(app_id, fbid, email, name):
    try:
        app_user = FBAppUser.objects.get(fb_app_id=app_id, fbid=fbid)
    except FBAppUser.DoesNotExist:
        try:
            ef_user = EFUser.objects.get(email=email)
        except EFUser.DoesNotExist:
            ef_user = EFUser(email=email, name=name)
        try:
            ef_user.save()
        except IntegrityError:
            ef_user = EFUser.objects.get(email=email)
        try:
            app_user = FBAppUser(fb_app_id=app_id, fbid=fbid, ef_user=ef_user)
            app_user.save()
        except IntegrityError:
            app_user = FBAppUser.objects.get(fb_app_id=app_id, fbid=fbid)

    return app_user.ef_user.efid
