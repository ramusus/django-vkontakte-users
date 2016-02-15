# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import annoying.fields


class Migration(migrations.Migration):

    dependencies = [
        ('vkontakte_users', '0002_auto_20160213_0238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='schools',
            field=annoying.fields.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='universities',
            field=annoying.fields.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
