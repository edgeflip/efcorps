from django.db import IntegrityError
from django.test import TestCase

from magnus import models
from magnus.models import operations


class TestGetOrCreateEfid(TestCase):

    def setUp(self):
        self.ef_user = models.EFUser.objects.create(name='Test Testerson',
                                                    email='test@testerson.net')
        self.fb_app = models.FBApp.objects.create(
            fb_app_id=10101010101,
            namespace='test-for-good',
            secret='sekr3t',
        )
        self.fb_app_user = self.fb_app.fb_app_users.create(ef_user=self.ef_user,
                                                           fbid=109090901)

    def test_app_user_exists(self):
        efid = operations.get_or_create_efid(self.fb_app.fb_app_id, self.fb_app_user.fbid,
                                             self.ef_user.email, self.ef_user.name)
        self.assertEqual(efid, self.ef_user.efid)
        self.assertEqual(models.EFUser.objects.count(), 1)
        self.assertEqual(models.FBAppUser.objects.count(), 1)

    def test_ef_user_new_app_user(self):
        fb_app = models.FBApp.objects.create(
            fb_app_id=90909090909,
            namespace='test-it-all',
            secret='sekr3t',
        )
        efid = operations.get_or_create_efid(fb_app.fb_app_id, 709090907,
                                             self.ef_user.email, self.ef_user.name)
        self.assertEqual(efid, self.ef_user.efid)
        self.assertEqual(models.EFUser.objects.count(), 1)
        self.assertEqual(models.FBAppUser.objects.count(), 2)

        fb_app_user = fb_app.fb_app_users.get()
        self.assertEqual(fb_app_user.fbid, 709090907)

    def test_new_user(self):
        self.ef_user.delete()
        self.fb_app_user.delete()
        efid = operations.get_or_create_efid(self.fb_app.fb_app_id, self.fb_app_user.fbid,
                                             self.ef_user.email, self.ef_user.name)
        self.assertNotEqual(efid, self.ef_user.efid) # serial field
        self.assertEqual(models.EFUser.objects.count(), 1)
        self.assertEqual(models.FBAppUser.objects.count(), 1)
        self.assertEqual(models.EFUser.objects.values('efid', 'email', 'name').get(), {
            'efid': efid,
            'email': self.ef_user.email,
            'name': self.ef_user.name,
        })

    def test_no_email_new_app_user(self):
        fb_app = models.FBApp.objects.create(
            fb_app_id=90909090909,
            namespace='test-it-all',
            secret='sekr3t',
        )
        fbid = 709090907
        efid = operations.get_or_create_efid(fb_app.fb_app_id, fbid,
                                             None, self.ef_user.name)
        self.assertNotEqual(efid, self.ef_user.efid)
        self.assertEqual(models.EFUser.objects.count(), 2)
        self.assertEqual(models.FBAppUser.objects.count(), 2)
        self.assertEqual(models.EFUser.objects.values('email', 'name').get(efid=efid), {
            'email': None,
            'name': self.ef_user.name,
        })

        fb_app_user = fb_app.fb_app_users.get()
        self.assertEqual(fb_app_user.fbid, fbid)

    def test_ef_user_fb_app_multiple_assignment(self):
        with self.assertRaises(IntegrityError):
            operations.get_or_create_efid(self.fb_app.fb_app_id, 709090907,
                                          self.ef_user.email, self.ef_user.name)
