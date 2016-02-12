# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vkontakte_users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='instagram',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='is_banned',
            field=models.BooleanField(default=False, verbose_name='\u0417\u0430\u0431\u0430\u043d\u0435\u043d'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='\u0423\u0434\u0430\u043b\u0435\u043d'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='schools',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='universities',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='bdate',
            field=models.CharField(max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='facebook',
            field=models.CharField(max_length=18),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='facebook_name',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='faculty_name',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=32),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='has_avatar',
            field=models.BooleanField(default=True, db_index=True, verbose_name='\u0415\u0441\u0442\u044c \u0430\u0432\u0430\u0442\u0430\u0440'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='home_phone',
            field=models.CharField(max_length=24),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='is_deactivated',
            field=models.BooleanField(default=False, db_index=True, verbose_name='\u0414\u0435\u0430\u043a\u0442\u0438\u0432\u0438\u0440\u043e\u0432\u0430\u043d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=32),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='livejournal',
            field=models.CharField(max_length=31),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile_phone',
            field=models.CharField(max_length=24),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='screen_name',
            field=models.CharField(max_length=32, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='skype',
            field=models.CharField(max_length=32),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='twitter',
            field=models.CharField(max_length=15),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='university_name',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
