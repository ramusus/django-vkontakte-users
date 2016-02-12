# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import vkontakte_api.models


class Migration(migrations.Migration):

    dependencies = [
        ('vkontakte_places', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('fetched', models.DateTimeField(db_index=True, null=True, verbose_name='\u041e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u043e', blank=True)),
                ('remote_id', models.BigIntegerField(help_text='\u0423\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440', serialize=False, verbose_name='ID', primary_key=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('screen_name', models.CharField(max_length=100, db_index=True)),
                ('sex', models.PositiveSmallIntegerField(db_index=True, null=True, choices=[(0, '\u043d\u0435 \u0443\u043a.'), (1, '\u0436\u0435\u043d.'), (2, '\u043c\u0443\u0436.')])),
                ('age', models.PositiveSmallIntegerField(null=True, db_index=True)),
                ('timezone', models.IntegerField(null=True)),
                ('rate', models.PositiveIntegerField(null=True, db_index=True)),
                ('bdate', models.CharField(max_length=100)),
                ('activity', models.TextField()),
                ('relation', models.SmallIntegerField(db_index=True, null=True, choices=[(1, '\u041d\u0435 \u0436\u0435\u043d\u0430\u0442 / \u0437\u0430\u043c\u0443\u0436\u0435\u043c'), (2, '\u0415\u0441\u0442\u044c \u0434\u0440\u0443\u0433 / \u043f\u043e\u0434\u0440\u0443\u0433\u0430'), (3, '\u041f\u043e\u043c\u043e\u043b\u0432\u043b\u0435\u043d / \u043f\u043e\u043c\u043e\u043b\u0432\u043b\u0435\u043d\u0430'), (4, '\u0416\u0435\u043d\u0430\u0442 / \u0437\u0430\u043c\u0443\u0436\u0435\u043c'), (5, '\u0412\u0441\u0451 \u0441\u043b\u043e\u0436\u043d\u043e'), (6, '\u0412 \u0430\u043a\u0442\u0438\u0432\u043d\u043e\u043c \u043f\u043e\u0438\u0441\u043a\u0435'), (7, '\u0412\u043b\u044e\u0431\u043b\u0451\u043d / \u0432\u043b\u044e\u0431\u043b\u0435\u043d\u0430')])),
                ('wall_comments', models.NullBooleanField()),
                ('graduation', models.PositiveIntegerField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f \u0432\u0443\u0437\u0430')),
                ('university', models.PositiveIntegerField(null=True)),
                ('university_name', models.CharField(max_length=500)),
                ('faculty', models.PositiveIntegerField(null=True)),
                ('faculty_name', models.CharField(max_length=500)),
                ('has_mobile', models.NullBooleanField(db_index=True)),
                ('home_phone', models.CharField(max_length=50)),
                ('mobile_phone', models.CharField(max_length=50)),
                ('photo', models.URLField()),
                ('photo_big', models.URLField()),
                ('photo_medium', models.URLField()),
                ('photo_medium_rec', models.URLField()),
                ('photo_rec', models.URLField()),
                ('twitter', models.CharField(max_length=500)),
                ('facebook', models.CharField(max_length=500)),
                ('facebook_name', models.CharField(max_length=500)),
                ('skype', models.CharField(max_length=500)),
                ('livejournal', models.CharField(max_length=500)),
                ('interests', models.TextField()),
                ('movies', models.TextField()),
                ('tv', models.TextField()),
                ('books', models.TextField()),
                ('games', models.TextField()),
                ('about', models.TextField()),
                ('friends_count', models.PositiveIntegerField(default=0, verbose_name='\u0414\u0440\u0443\u0437\u0435\u0439')),
                ('counters_updated', models.DateTimeField(help_text='\u0421\u0447\u0435\u0442\u0447\u0438\u043a\u0438 \u0431\u044b\u043b\u0438 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u044b', null=True, db_index=True)),
                ('sum_counters', models.PositiveIntegerField(default=0, help_text='\u0421\u0443\u043c\u043c\u0430 \u0432\u0441\u0435\u0445 \u0441\u0447\u0435\u0442\u0447\u0438\u043a\u043e\u0432')),
                ('albums', models.PositiveIntegerField(default=0, verbose_name='\u0424\u043e\u0442\u043e\u0430\u043b\u044c\u0431\u043e\u043c\u043e\u0432')),
                ('videos', models.PositiveIntegerField(default=0, verbose_name='\u0412\u0438\u0434\u0435\u043e\u0437\u0430\u043f\u0438\u0441\u0435\u0439')),
                ('audios', models.PositiveIntegerField(default=0, verbose_name='\u0410\u0443\u0434\u0438\u043e\u0437\u0430\u043f\u0438\u0441\u0435\u0439')),
                ('followers', models.PositiveIntegerField(default=0, verbose_name='\u041f\u043e\u0434\u043f\u0438\u0441\u0447\u0438\u043a\u043e\u0432')),
                ('friends', models.PositiveIntegerField(default=0, verbose_name='\u0414\u0440\u0443\u0437\u0435\u0439', db_index=True)),
                ('mutual_friends', models.PositiveIntegerField(default=0, verbose_name='\u041e\u0431\u0449\u0438\u0445 \u0434\u0440\u0443\u0437\u0435\u0439')),
                ('notes', models.PositiveIntegerField(default=0, verbose_name='\u0417\u0430\u043c\u0435\u0442\u043e\u043a')),
                ('subscriptions', models.PositiveIntegerField(default=0, verbose_name='\u041f\u043e\u0434\u043f\u0438\u0441\u043e\u043a (\u0442\u043e\u043b\u044c\u043a\u043e \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438)')),
                ('user_photos', models.PositiveIntegerField(default=0, verbose_name='\u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0439 \u0441 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u043c')),
                ('user_videos', models.PositiveIntegerField(default=0, verbose_name='\u0412\u0438\u0434\u0435\u043e\u0437\u0430\u043f\u0438\u0441\u0435\u0439 \u0441 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u043c')),
                ('is_deactivated', models.BooleanField(default=False, db_index=True, verbose_name='\u0414\u0435\u0430\u043a\u0442\u0438\u0432\u0438\u0440\u043e\u0432\u0430\u043d?')),
                ('has_avatar', models.BooleanField(default=True, db_index=True, verbose_name='\u0415\u0441\u0442\u044c \u0430\u0432\u0430\u0442\u0430\u0440?')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='vkontakte_places.City', null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='vkontakte_places.Country', null=True)),
                ('friends_users', models.ManyToManyField(related_name='followers_users', to='vkontakte_users.User')),
            ],
            options={
                'verbose_name': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c \u0412\u043a\u043e\u043d\u0442\u0430\u043a\u0442\u0435',
                'verbose_name_plural': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438 \u0412\u043a\u043e\u043d\u0442\u0430\u043a\u0442\u0435',
            },
            bases=(vkontakte_api.models.RemoteIdModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='UserRelative',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=20, verbose_name='\u0422\u0438\u043f \u0440\u043e\u0434\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0439 \u0441\u0432\u044f\u0437\u0438', choices=[(b'grandchild', '\u0432\u043d\u0443\u043a/\u0432\u043d\u0443\u0447\u043a\u0430'), (b'grandparent', '\u0434\u0435\u0434\u0443\u0448\u043a\u0430/\u0431\u0430\u0431\u0443\u0448\u043a\u0430'), (b'child', '\u0441\u044b\u043d/\u0434\u043e\u0447\u043a\u0430'), (b'sibling', '\u0431\u0440\u0430\u0442/\u0441\u0435\u0441\u0442\u0440\u0430'), (b'parent', '\u043c\u0430\u043c\u0430/\u043f\u0430\u043f\u0430')])),
                ('user1', models.ForeignKey(related_name='user_relatives1', to='vkontakte_users.User')),
                ('user2', models.ForeignKey(related_name='user_relatives2', to='vkontakte_users.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
