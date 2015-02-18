# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('magnus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='client',
            field=models.ForeignKey(related_name='campaigns', blank=True, to='magnus.Client', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fbappuser',
            name='person',
            field=models.ForeignKey(to='magnus.Person', db_column=b'efid'),
            preserve_default=True,
        ),
    ]
